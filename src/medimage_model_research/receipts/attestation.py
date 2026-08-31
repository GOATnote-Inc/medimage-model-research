"""Receipts attestation skeleton.

Every training run + checkpoint + release in this repo writes an attestation
with the NC obligation field PROMINENTLY flagged so downstream consumers can
never accidentally treat the weights as commercial-OK.

This is the on-disk format. The wire format to the `receipts` ledger lands in
PR #2 when the HTTP client is integrated.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

# Matches a standalone "NC" token (CC BY-NC-SA, CC-BY-NC-4.0, "NC"), spelled-out
# non-commercial in any casing/spacing, and research/academic-restricted terms.
# Over-matching is acceptable: a false positive marks weights research-only,
# which is the safe direction.
_NC_PATTERN = re.compile(
    r"(?:^|[^a-z0-9])nc(?:[^a-z0-9]|$)|non[\s-]?commercial|research|academic",
    re.IGNORECASE,
)


def license_implies_nc(license_text: str) -> bool:
    """True when a license string indicates a non-commercial/research restriction.

    Normalised, case-insensitive matching. "CC BY-NC-SA 4.0", "non-commercial",
    "NonCommercial", "research-only", and "academic use" all return True;
    "CC-BY-4.0" and "Apache-2.0" return False.
    """
    return bool(_NC_PATTERN.search(license_text))


@dataclass(frozen=True)
class TrainingDataProvenance:
    """Provenance facts about the training corpus that produced a checkpoint."""

    access_log_sha256: str
    access_log_path: str
    n_records: int
    licenses: tuple[str, ...]
    providers: tuple[str, ...]
    nc_obligation: bool


@dataclass(frozen=True)
class Attestation:
    """A single attestation row.

    Format intentionally simple and stable — once written, never edited.
    Append-only. Merkle root is computed from a canonical JSON serialisation.
    """

    schema_version: int
    artifact_kind: str  # "checkpoint" | "release" | "eval_run"
    artifact_id: str
    code_commit: str
    config_sha256: str
    training_data: TrainingDataProvenance
    eval_results_sha256: str
    judge_versions: tuple[str, ...]
    seed: int
    created_at_utc: str
    notes: str = ""

    def canonical_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def merkle_leaf(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


def hash_access_log(path: Path) -> tuple[str, int]:
    """Return (sha256_hex, n_records) for an access log JSONL."""
    if not path.exists():
        return hashlib.sha256(b"").hexdigest(), 0
    h = hashlib.sha256()
    n = 0
    with path.open("rb") as fh:
        for line in fh:
            if line.strip():
                h.update(line)
                n += 1
    return h.hexdigest(), n


def make_attestation(
    *,
    artifact_kind: str,
    artifact_id: str,
    code_commit: str,
    config_sha256: str,
    access_log: Path,
    eval_results_sha256: str,
    judge_versions: tuple[str, ...],
    seed: int,
    providers: tuple[str, ...] = ("Forithmus", "UZH", "Medipol", "NVIDIA"),
    licenses: tuple[str, ...] = ("CC-BY-NC-SA-4.0",),
    commercial_use: bool | None = None,
    notes: str = "",
) -> Attestation:
    """Build an Attestation from explicit fields + an access-log path.

    ``nc_obligation`` is the field downstream consumers MUST check, and it is
    computed fail-closed:

    * ``commercial_use=False`` (caller knows the terms forbid commercial use)
      forces True.
    * Any license string matching a non-commercial/research marker
      (see ``license_implies_nc``) forces True — even when the caller passed
      ``commercial_use=True``; the recorded terms win over the caller's claim.
    * An empty ``licenses`` tuple forces True: no recorded license information
      is never grounds for treating weights as commercial-OK.
    * Only ``commercial_use=True`` (or None) with non-empty, cleanly
      permissive license strings yields False.
    """
    access_log_hash, n_records = hash_access_log(access_log)
    nc_obligation = (
        commercial_use is False or not licenses or any(license_implies_nc(lic) for lic in licenses)
    )
    provenance = TrainingDataProvenance(
        access_log_sha256=access_log_hash,
        access_log_path=str(access_log),
        n_records=n_records,
        licenses=licenses,
        providers=providers,
        nc_obligation=nc_obligation,
    )
    return Attestation(
        schema_version=1,
        artifact_kind=artifact_kind,
        artifact_id=artifact_id,
        code_commit=code_commit,
        config_sha256=config_sha256,
        training_data=provenance,
        eval_results_sha256=eval_results_sha256,
        judge_versions=judge_versions,
        seed=seed,
        created_at_utc=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        notes=notes,
    )
