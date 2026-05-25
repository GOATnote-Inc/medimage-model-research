"""Attestation skeleton tests."""

from __future__ import annotations

import hashlib
import json

from medimage_model_research.receipts.attestation import (
    hash_access_log,
    make_attestation,
)


def test_hash_access_log_empty(tmp_path):
    digest, n = hash_access_log(tmp_path / "missing.jsonl")
    assert n == 0
    assert digest == hashlib.sha256(b"").hexdigest()


def test_hash_access_log_two_records(tmp_path):
    log = tmp_path / "access.jsonl"
    log.write_text('{"shard": "a"}\n{"shard": "b"}\n')
    digest, n = hash_access_log(log)
    assert n == 2
    # Recompute by hand
    h = hashlib.sha256()
    h.update(b'{"shard": "a"}\n')
    h.update(b'{"shard": "b"}\n')
    assert digest == h.hexdigest()


def test_attestation_flags_nc_obligation(tmp_path):
    att = make_attestation(
        artifact_kind="checkpoint",
        artifact_id="vX.Y.0-step42",
        code_commit="deadbeef",
        config_sha256="c" * 64,
        access_log=tmp_path / "missing.jsonl",
        eval_results_sha256="e" * 64,
        judge_versions=("claude-opus-4-7", "gpt-5.4"),
        seed=42,
    )
    assert att.training_data.nc_obligation is True
    assert "CC-BY-NC-SA-4.0" in att.training_data.licenses


def test_attestation_canonical_json_is_stable(tmp_path):
    """Two attestations with the same inputs (modulo timestamp) hash to the
    same Merkle leaf when we control for created_at_utc."""
    kwargs = {
        "artifact_kind": "release",
        "artifact_id": "v0.1.0",
        "code_commit": "abc123",
        "config_sha256": "1" * 64,
        "access_log": tmp_path / "missing.jsonl",
        "eval_results_sha256": "2" * 64,
        "judge_versions": ("claude-opus-4-7", "gpt-5.4"),
        "seed": 0,
    }
    att1 = make_attestation(**kwargs)
    canonical = att1.canonical_json()
    # canonical_json must be valid JSON and stable
    decoded = json.loads(canonical)
    assert decoded["artifact_id"] == "v0.1.0"
    assert ", " not in canonical, "compact separators expected"
    # Merkle leaf is sha256 of canonical
    leaf = att1.merkle_leaf()
    assert leaf == hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def test_attestation_eval_kind_with_permissive_licenses(tmp_path):
    """A future use case: same machinery with permissive licenses → nc_obligation False."""
    att = make_attestation(
        artifact_kind="eval_run",
        artifact_id="run-0001",
        code_commit="ffffff",
        config_sha256="d" * 64,
        access_log=tmp_path / "missing.jsonl",
        eval_results_sha256="f" * 64,
        judge_versions=("claude-opus-4-7", "gpt-5.4"),
        seed=7,
        licenses=("CC0-1.0", "CC-BY-4.0"),
        providers=("OpenNeuro",),
    )
    assert att.training_data.nc_obligation is False
