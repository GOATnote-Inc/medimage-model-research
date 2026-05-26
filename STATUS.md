# STATUS

## Active task
**v0.2 — CT-RATE access mirror + receipts wire-up.** The scaffold and the MR-RATE two-gate access pattern are merged. Next is replicating the same pattern for CT-RATE and connecting the receipts client.

## Exit criteria for current pickup
- `src/medimage_model_research/data/ct_rate.py` mirrors `mr_rate.py` — same two-gate preflight (NC ack + HF_TOKEN), same access record schema, same CC BY-NC-SA license attached, same `redistribute=false`
- `src/medimage_model_research/receipts/client.py` POSTs an `Attestation` to a configurable ledger URL (stubbed HTTP for now; real receipts ledger integration when the wire format is finalised)
- Hermetic tests cover both: CT-RATE gating + receipts roundtrip with mock HTTP
- `make lint` green; `make test` green

## Verify command
```
make lint && make test
```

## Already shipped (do not re-do)
- **PR #1** — Two-gate MR-RATE access loader (`NCAcknowledgementMissingError` + `HuggingFaceTokenMissingError`, length-only token reporting), `nc_acknowledge.py` per-developer opt-in with SHA-256 of terms text, `Attestation` skeleton with `TrainingDataProvenance.nc_obligation` auto-flag for any NC license in the input, deterministic canonical JSON for Merkle leaves, `nc_boundary_check.py` CI gate that refuses any NIfTI/DICOM/safetensors blobs in tree

## Next-up after this pickup
1. medimage-eval substrate integration (same shape as `medimage-model`)
2. Comparative-eval scaffolding against the commercial-OK track (same eval, two models → published delta)
3. First contrastive-pretraining smoke run on synthetic inputs
4. Federated-training scaffold for partner-hospital data

## Hard constraints
- **NEVER redistribute MR-RATE / CT-RATE.** Section 5 of MR-RATE license forbids it; CI's `nc_boundary_check.py` enforces.
- `data/mr_rate/`, `data/ct_rate/` are gitignored and STAY gitignored
- Every model checkpoint's attestation MUST carry `data_license: "CC-BY-NC-SA-4.0"` and `nc_obligation: true`
- Commercial deployment of weights requires a Forithmus contract OR re-training on `medimage-model`'s permissive corpus
- Sibling commercial-OK repo is [`medimage-model`](https://github.com/GOATnote-Inc/medimage-model) — do NOT cross-pollinate data

## Branch protection
Not yet enabled on this repo. Follow-up: add the four-context baseline (lint, secrets-scan, unit, nc-boundary) once CT-RATE access ships.

## Last updated
2026-05-26 — end of scaffolding session (PR #1 merged)
