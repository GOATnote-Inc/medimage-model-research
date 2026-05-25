# STATUS

## Active task
**Bootstrap v0.1 scaffold.** Land MR-RATE access gating + NC-acknowledgement preflight + provenance attestation skeleton. No training yet.

## Exit criteria for current pickup
- `make lint` green
- `make test` green (hermetic)
- `scripts/nc_acknowledge.py` writes a local opt-in receipt and refuses ingestion when missing
- `src/medimage_model_research/data/mr_rate.py` exposes a gated-access fetcher that reads HF_TOKEN from env and refuses to proceed without a valid NC acknowledgement

## Verify command
```
make lint && make test
```

## Next-up after pickup
1. CT-RATE access gating mirror.
2. Receipts attestation writer with `data_license` field.
3. First contrastive-pretraining smoke run (synthetic inputs).
4. Comparative-eval scaffolding against `medimage-model`.

## Known blockers
None.

## Last updated
2026-05-25 — initial scaffold
