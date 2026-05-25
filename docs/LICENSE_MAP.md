# License map

## Code
**Apache License 2.0**.

## Training data
This repo intentionally ingests **research-only** corpora.

| Dataset | License | Commercial use? | Source |
|---|---|---|---|
| MR-RATE | CC BY-NC-SA 4.0 | No (without Forithmus contract) | [HuggingFace](https://huggingface.co/datasets/Forithmus/MR-RATE) |
| CT-RATE | CC BY-NC-SA 4.0 | No | [HuggingFace](https://huggingface.co/datasets/ibrahimhamamci/CT-RATE) |
| ABIDE | CC BY-NC-SA 4.0 | No | various |
| (other permissive corpora may be added too — same SPDX rules as commercial track) | | | |

## Trained model weights
**Research-only.** Inherited from CC BY-NC-SA on the training data. Released per release under:

```
NVIDIA Open Model License — Research Use Only Addendum
```

The plain Apache-2.0 / NVIDIA Open Model License options are **not** available for these weights because of the upstream data constraint. To unblock commercial deployment, two paths exist:

1. Negotiate a commercial license with Forithmus (and any other NC data providers in the training mix).
2. Re-train under `medimage-model` using only permissive data (the parallel commercial track).

## Synthetic samples
NV-Generate-MR-Brain weights are themselves NVIDIA Open Model License (commercial-OK per NVIDIA). When used in this repo, however, the synthetic samples are mixed with NC real data, so the resulting model still inherits the NC constraint.
