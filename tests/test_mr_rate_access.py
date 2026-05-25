"""MR-RATE gated-access tests.

All hermetic — no network. We check that the preflight refuses to proceed
unless both the NC acknowledgement AND HF_TOKEN are in place, and that the
access-log writer round-trips a record.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medimage_model_research.data.mr_rate import (
    HuggingFaceTokenMissingError,
    MRRateAccessRecord,
    MRRateLoaderConfig,
    NCAcknowledgementMissingError,
    preflight,
    record_access,
)


def _cfg(tmp_path: Path, ack_present: bool = True) -> MRRateLoaderConfig:
    ack_path = tmp_path / "nc_ack.json"
    if ack_present:
        ack_path.write_text('{"version": 1}')
    return MRRateLoaderConfig(
        local_root=tmp_path / "mr_rate",
        access_log=tmp_path / "access.jsonl",
        nc_ack_path=ack_path,
    )


def test_preflight_refuses_without_nc_ack(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "hf_fake_token_12345")
    cfg = _cfg(tmp_path, ack_present=False)
    with pytest.raises(NCAcknowledgementMissingError):
        preflight(cfg)


def test_preflight_refuses_without_hf_token(tmp_path, monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    cfg = _cfg(tmp_path, ack_present=True)
    with pytest.raises(HuggingFaceTokenMissingError):
        preflight(cfg)


def test_preflight_passes_with_both_gates(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "hf_fake_token_12345")
    cfg = _cfg(tmp_path, ack_present=True)
    status = preflight(cfg)
    assert status["nc_ack"] is True
    assert status["hf_token_len"] == len("hf_fake_token_12345")


def test_preflight_never_returns_token_value(tmp_path, monkeypatch):
    secret = "hf_extra_secret_value_do_not_leak"
    monkeypatch.setenv("HF_TOKEN", secret)
    cfg = _cfg(tmp_path, ack_present=True)
    status = preflight(cfg)
    assert secret not in str(status)
    assert secret not in str(list(status.values()))


def test_record_access_appends(tmp_path):
    cfg = _cfg(tmp_path, ack_present=True)
    rec1 = MRRateAccessRecord(
        repo_id="Forithmus/MR-RATE",
        revision="main",
        shard="shard-0001.tar",
        sha256="a" * 64,
        bytes=12345,
        accessed_at_utc="2026-05-25T00:00:00+00:00",
    )
    rec2 = MRRateAccessRecord(
        repo_id="Forithmus/MR-RATE",
        revision="main",
        shard="shard-0002.tar",
        sha256="b" * 64,
        bytes=67890,
        accessed_at_utc="2026-05-25T00:00:01+00:00",
    )
    record_access(rec1, cfg)
    record_access(rec2, cfg)
    lines = cfg.access_log.read_text().strip().split("\n")
    assert len(lines) == 2
    parsed = [json.loads(line) for line in lines]
    assert parsed[0]["shard"] == "shard-0001.tar"
    assert parsed[1]["shard"] == "shard-0002.tar"
    # NC license carried on every record by default
    assert all(r["license"] == "CC-BY-NC-SA-4.0" for r in parsed)
    assert all(r["redistribution_allowed"] is False for r in parsed)
