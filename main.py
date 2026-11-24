#!/usr/bin/env python3
"""THE GLOBAL DISPATCH — entry runner for news-image-20261123 (akun5).

The artwork itself (entry.png, drawn in this session by compose.py) is the
entry. This runner is deliberately boring: standard library only, no image
libraries, it verifies the PNG sitting next to it and copies it verbatim to
the output directory the harness points at. Two runs give the same bytes.

Guards: PNG magic, the 1 MiB competition ceiling, and an exact byte count
plus SHA-256 of the shipped artwork so a swapped or truncated file fails
loudly instead of submitting the wrong front page.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 113630
EXPECTED_SHA256 = "f18b81a10d06d0447e1fe1d3359629ececa4f8d3f27b16fe2d833c2a3406ac57"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
CEILING = 1048576  # 1 MiB hard gate for this competition


def load_artwork(path):
    # Read the whole artwork in one go; it is ~114 KB, far below the gate.
    with open(path, "rb") as fh:
        return fh.read()


def check_artwork(blob):
    if not blob:
        raise SystemExit("entry.png is empty")
    if blob[:8] != PNG_HEADER:
        raise SystemExit("entry.png does not start with the PNG magic bytes")
    if len(blob) > CEILING:
        raise SystemExit("entry.png is over the 1 MiB gate: %d bytes" % len(blob))
    if len(blob) != EXPECTED_BYTES:
        raise SystemExit(
            "entry.png size drifted: got %d, expected %d"
            % (len(blob), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.png sha256 drifted: %s" % digest)
    return digest


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    blob = load_artwork(os.path.join(here, "entry.png"))
    digest = check_artwork(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(blob)
    sys.stderr.write("wrote %s (%d bytes, sha256=%s)\n" % (target, len(blob), digest))


if __name__ == "__main__":
    main()
