#!/usr/bin/env python3
"""Record (or verify) the NC-acknowledgement opt-in for this developer.

Before any code in this repo can fetch MR-RATE / CT-RATE data, the human
operator must run:

    python scripts/nc_acknowledge.py

This writes `~/.medimage-research/nc_ack.json` with the timestamp + the SHA-256
of the NC terms text on file. Data loaders refuse to proceed unless the file is
present and the hashes match the current terms.

Run with `--check` to verify the acknowledgement is on file without re-running
the prompt (used by `make preflight`).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

from medimage_model_research.nc_terms import NC_TERMS_TEXT, terms_hash

ACK_PATH = Path.home() / ".medimage-research" / "nc_ack.json"


def _terms_hash() -> str:
    return terms_hash()


def write_ack() -> int:
    print(NC_TERMS_TEXT)
    sys.stdout.write('Type "I AGREE" to record the acknowledgement: ')
    sys.stdout.flush()
    response = sys.stdin.readline().strip()
    if response != "I AGREE":
        print("Acknowledgement not recorded.", file=sys.stderr)
        return 1
    ACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    ACK_PATH.write_text(
        json.dumps(
            {
                "user": os.environ.get("USER", "unknown"),
                "timestamp_utc": dt.datetime.now(dt.UTC).isoformat(),
                "terms_sha256": _terms_hash(),
                "version": 1,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"Acknowledgement recorded at {ACK_PATH}")
    return 0


def check_ack() -> int:
    if not ACK_PATH.exists():
        print(f"NC acknowledgement missing at {ACK_PATH}", file=sys.stderr)
        print("Run `make nc-ack` to record one.", file=sys.stderr)
        return 2
    data = json.loads(ACK_PATH.read_text())
    if data.get("terms_sha256") != _terms_hash():
        print("NC acknowledgement terms have changed since last opt-in.", file=sys.stderr)
        print("Re-run `make nc-ack` to re-acknowledge.", file=sys.stderr)
        return 3
    print(f"NC acknowledgement OK ({ACK_PATH})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 0 if ack present and current; non-zero otherwise",
    )
    args = parser.parse_args()
    if args.check:
        return check_ack()
    return write_ack()


if __name__ == "__main__":
    raise SystemExit(main())
