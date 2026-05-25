#!/usr/bin/env python3
"""NC-boundary CI gate.

This repo intentionally consumes CC BY-NC-SA data (MR-RATE, CT-RATE). The
boundary that MUST hold:

  * The data itself is never committed (gitignored).
  * `data/mr_rate/`, `data/ct_rate/`, etc. are gitignored.
  * No NIfTI / DICOM / safetensors blobs are committed.

This check walks the working tree and fails CI if any of those appear.
"""

from __future__ import annotations

import sys
from pathlib import Path

# File extensions that should never be committed to this repo.
BLOCKED_EXTENSIONS = {".nii", ".nii.gz", ".dcm", ".safetensors", ".bin", ".pt", ".pth"}

# Paths that should never exist as tracked content.
BLOCKED_PATH_FRAGMENTS = (
    "data/mr_rate/",
    "data/ct_rate/",
    "data/raw/",
    "checkpoints/",
)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    offenders: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if any(rel.startswith(fragment) for fragment in BLOCKED_PATH_FRAGMENTS):
            offenders.append(rel)
            continue
        if any(path.name.endswith(ext) for ext in BLOCKED_EXTENSIONS):
            offenders.append(rel)

    if offenders:
        print("NC boundary violated — these files must NOT be in the repo:", file=sys.stderr)
        for o in offenders:
            print(f"  - {o}", file=sys.stderr)
        return 2

    print("NC boundary clean: no NC-licensed data or model blobs in tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
