# medimage-model-research

**Research-track brain-MR multimodal reasoning model, trained on MR-RATE + CT-RATE.**

The NC-constrained sibling of [`medimage-model`](https://github.com/GOATnote-Inc/medimage-model). Same architecture, same [`medimage-eval`](https://github.com/GOATnote-Inc/medimage-eval) substrate, but ingests CC BY-NC-SA training corpora (MR-RATE, CT-RATE). Weights from this repo are **research-only** — commercial use requires separate contracts with the data providers (Forithmus et al.).

> Status: pre-v0.1 scaffold. See `docs/LICENSE_MAP.md` for the constraint chain.

## Why a separate repo
Maintaining a clean license boundary. The commercial-OK track (`medimage-model`) must never see CC BY-NC-SA data. Putting MR-RATE-trained work here makes that boundary visible at the repo level, not just at the manifest level.

## What changes vs `medimage-model`
- Adds MR-RATE + CT-RATE manifests (gated HuggingFace access)
- Replaces the license preflight with an **NC-acknowledgement preflight** that requires explicit opt-in
- Receipts attestation includes a "data license" field flagging downstream NC obligations
- Otherwise architecturally identical: MAISI-v2 + Nemotron-3-Nano-30B-A3B + Megatron+SGLang+GRPO

## License
Code: **Apache License 2.0**. Trained weights: **research-only** per upstream CC BY-NC-SA constraints. See `docs/LICENSE_MAP.md`.
