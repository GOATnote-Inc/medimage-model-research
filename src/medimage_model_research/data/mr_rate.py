"""MR-RATE gated-access loader.

MR-RATE is CC BY-NC-SA 4.0. The dataset itself is gated behind a HuggingFace
contact-info form, and our internal discipline adds a second gate: a per-user
NC-acknowledgement opt-in (`scripts/nc_acknowledge.py`). This module enforces
BOTH gates before any data fetch can proceed.

We do not redistribute MR-RATE through this repo. Files land under `data/mr_rate/`
which is gitignored, and a manifest of accessed shards is written to
`data/manifests/mr_rate_access.jsonl` (append-only) for provenance.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


class NCAcknowledgementMissingError(RuntimeError):
    """Raised when the NC acknowledgement opt-in is not on file."""


class HuggingFaceTokenMissingError(RuntimeError):
    """Raised when HF_TOKEN is absent — MR-RATE access requires a gated-token."""


@dataclass(frozen=True)
class MRRateAccessRecord:
    """One row of the MR-RATE access manifest."""

    repo_id: str
    revision: str
    shard: str
    sha256: str
    bytes: int
    accessed_at_utc: str
    license: str = "CC-BY-NC-SA-4.0"
    redistribution_allowed: bool = False
    notes: str = ""


@dataclass
class MRRateLoaderConfig:
    """Configuration for the MR-RATE loader."""

    repo_id: str = "Forithmus/MR-RATE"
    revision: str = "main"
    local_root: Path = field(default_factory=lambda: Path("data/mr_rate"))
    access_log: Path = field(
        default_factory=lambda: Path("data/manifests/mr_rate_access.jsonl")
    )
    nc_ack_path: Path = field(default_factory=lambda: Path.home() / ".medimage-research" / "nc_ack.json")
    hf_token_env: str = "HF_TOKEN"


def _check_nc_ack(path: Path) -> None:
    if not path.exists():
        raise NCAcknowledgementMissingError(
            f"NC acknowledgement missing at {path}. Run `make nc-ack` first."
        )


def _check_hf_token(env_var: str) -> str:
    token = os.environ.get(env_var, "")
    if not token:
        raise HuggingFaceTokenMissingError(
            f"{env_var} not set. Set it from a credentialed source (do not commit)."
        )
    return token


def preflight(config: Optional[MRRateLoaderConfig] = None) -> dict:
    """Verify both gates without performing any network calls.

    Returns a dict with `{nc_ack: bool, hf_token_len: int}`. Raises on failure.
    Never returns or logs the token value itself.
    """
    cfg = config or MRRateLoaderConfig()
    _check_nc_ack(cfg.nc_ack_path)
    token = _check_hf_token(cfg.hf_token_env)
    return {"nc_ack": True, "hf_token_len": len(token)}


def record_access(record: MRRateAccessRecord, config: Optional[MRRateLoaderConfig] = None) -> None:
    """Append one access record to the JSONL access log.

    This is the provenance trail. Every shard fetched must land a row. The
    receipts attestation later hashes this file to seal training-data provenance.
    """
    cfg = config or MRRateLoaderConfig()
    cfg.access_log.parent.mkdir(parents=True, exist_ok=True)
    with cfg.access_log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(record), sort_keys=True) + "\n")
