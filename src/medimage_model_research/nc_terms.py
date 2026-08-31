"""Canonical NC-acknowledgement terms, shared by the opt-in script and the loaders.

Both `scripts/nc_acknowledge.py` (which records the acknowledgement) and
`data/mr_rate.py` (which enforces it) hash this exact text. Changing the terms
invalidates every existing acknowledgement, forcing re-acknowledgement —
that is intentional.
"""

from __future__ import annotations

import hashlib

NC_TERMS_TEXT = """\
I acknowledge that:

1. MR-RATE and CT-RATE are licensed under CC BY-NC-SA 4.0.
2. Any model weights trained in this repository may inherit the
   non-commercial constraint from the training data.
3. I will not redistribute the datasets or use derived models for
   commercial purposes without separate agreements with the dataset
   providers (Forithmus and co-licensors).
4. Outputs from these models will be marked research-only in any
   downstream artifact.
"""


def terms_hash() -> str:
    """SHA-256 of the canonical terms text."""
    return hashlib.sha256(NC_TERMS_TEXT.encode("utf-8")).hexdigest()
