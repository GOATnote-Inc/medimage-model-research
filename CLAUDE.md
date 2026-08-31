# CLAUDE.md — medimage-model-research operating charter

## Mission
Research-track sibling of `medimage-model`. Same architecture, same eval substrate, but uses MR-RATE + CT-RATE (CC BY-NC-SA) for SOTA chase + publication.

## Non-negotiables

1. **NC acknowledgement required at ingest.** Every contributor must run `scripts/nc_acknowledge.py` once before any data ingest. The script writes a local opt-in receipt.
2. **No redistribution of MR-RATE / CT-RATE.** Section 5 of the MR-RATE license forbids it. We download into `data/mr_rate/` (gitignored) and never push.
3. **Every model checkpoint carries the NC obligation.** Receipts attestation flags `data_license: "CC-BY-NC-SA-4.0"` so downstream consumers cannot accidentally bypass.
4. **No `.env` reads.** HF tokens and judge keys come from the environment; verify presence with length-only checks, never print values.
5. **No `git add -A`.** Stage by name. `data/`, `checkpoints/`, `wandb/`, `eval_outputs/` are gitignored.
6. **Judge pre-flight before multi-hour runs.** Same lesson as the other repos.

## Continuation contract
- Start: read `STATUS.md`.
- End: update `STATUS.md`.

## Sibling repos
- `medimage-model` — commercial-OK track, do NOT cross-contaminate data.
- `medimage-eval` — substrate (shared dependency).
- `medimage-corpus` — dataset catalog (reference only).
