# Architecture

Architecturally identical to [`medimage-model`](https://github.com/GOATnote-Inc/medimage-model). Only the data layer and the receipts attestation field set differ.

## Data layer differences vs commercial-OK track
- Adds MR-RATE (Forithmus + UZH) and CT-RATE (Hamamci et al.) via gated HuggingFace access.
- Requires the NC-acknowledgement preflight before ingestion.
- All MR-RATE / CT-RATE storage lives under `data/mr_rate/` and `data/ct_rate/` — gitignored.

## Receipts attestation differences
Each release attestation carries:
- `data_license: "CC-BY-NC-SA-4.0"`
- `commercial_use: false`
- `data_providers: ["Forithmus", "UZH", "Medipol", "NVIDIA"]`

These flags propagate into the model card so downstream consumers cannot accidentally treat the weights as commercial-OK.

## Eval substrate
Shared with `medimage-model`. Direct comparison between the two tracks is the whole point — measure how much SOTA the NC corpus actually buys after the commercial-OK substrate maxes out.
