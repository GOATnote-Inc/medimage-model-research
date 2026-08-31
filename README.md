# medimage-model-research

**NC-track scaffold for a planned research brain-MR multimodal model. No weights, no training code, and no dataset manifests exist here yet.**

The NC-constrained sibling of [`medimage-model`](https://github.com/GOATnote-Inc/medimage-model). The plan: same architecture and the same [`medimage-eval`](https://github.com/GOATnote-Inc/medimage-eval) substrate, but ingesting CC BY-NC-SA training corpora (MR-RATE, CT-RATE). Weights eventually trained here would be **research-only** — commercial use requires separate contracts with the data providers (Forithmus and co-licensors).

> Status: pre-v0.1 scaffold. See `docs/LICENSE_MAP.md` for the constraint chain and `STATUS.md` for the dated state.

## Why a separate repo

Maintaining a clean license boundary. The commercial-OK track (`medimage-model`) must never see CC BY-NC-SA data. Putting MR-RATE-derived work here makes that boundary visible at the repo level, not just at the manifest level.

## Implemented

- **Two-gate MR-RATE access preflight** (`src/medimage_model_research/data/mr_rate.py`) — refuses to proceed unless (1) a per-user NC acknowledgement is on file **and its recorded terms hash matches the current terms**, and (2) `HF_TOKEN` is present (checked length-only, never echoed). No download code exists yet; this is the gate the future loader must pass through.
- **NC acknowledgement opt-in** (`scripts/nc_acknowledge.py`, `make nc-ack`) — interactive "I AGREE" prompt that records a timestamped receipt with the SHA-256 of the terms text (canonical text lives in `medimage_model_research.nc_terms`, shared by the recorder and the enforcing gate).
- **Append-only access log** — JSONL writer for per-shard provenance records (repo id, revision, sha256, license), written under gitignored `data/`.
- **Attestation skeleton** (`receipts/attestation.py`) — canonical-JSON leaf hash plus a fail-closed `nc_obligation` flag: normalised license-text matching (`license_implies_nc`), an explicit `commercial_use` input, and "no license recorded" treated as NC. Downstream consumers must check this field.
- **NC boundary CI check** (`scripts/nc_boundary_check.py`) — refuses imaging/weight blobs in the tree.

## Planned (not yet built)

- MR-RATE / CT-RATE dataset manifests and an actual gated fetch path (`huggingface_hub`, pinned revisions, per-shard hashes into the access log)
- Model, training (SFT + GRPO), serving, and eval wire-up to `medimage-eval` (declared as a pinned optional extra; not yet consumed by any code)
- Receipts ledger integration for attestations

## Not for clinical use

Nothing here is a medical device. Any future model outputs are research artifacts and must not be used for diagnosis or treatment decisions.

## License

Code: **Apache License 2.0** (full text in `LICENSE`). Trained weights (future): **research-only** per upstream CC BY-NC-SA constraints — see `NOTICE` and `docs/LICENSE_MAP.md`.
