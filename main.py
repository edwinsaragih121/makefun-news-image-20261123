#!/usr/bin/env python3
"""Entry runner — THE GLOBAL DISPATCH (akun5, news-image-20261123).

The front page is the program's whole payload: entry.png, a 1024x1024
broadsheet of Monday 23 November 2026 drawn by compose.py in this repo.
This file's single job is to hand that page to the harness untouched.

It leans on nothing outside the standard library and never decodes the
image — it reads the bytes, checks them against the size and SHA-256 the
page shipped with, and writes them to $MAKEFUN_OUTPUT_DIR/entry.png (or
/output when the variable is unset). Same input, same output, every run.
"""

import hashlib
import os
import sys

PAGE_BYTES = 113630
PAGE_SHA256 = "f18b81a10d06d0447e1fe1d3359629ececa4f8d3f27b16fe2d833c2a3406ac57"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
HARD_LIMIT = 1048576


def read_page(folder):
    # The page is small (~114 KB); a single read keeps the copy byte-exact.
    path = os.path.join(folder, "entry.png")
    with open(path, "rb") as fh:
        return fh.read()


def verify_page(blob):
    """Refuse to ship anything that is not exactly the drawn front page."""
    if len(blob) == 0:
        sys.exit("entry.png is empty — nothing to submit")
    if not blob.startswith(PNG_SIGNATURE):
        sys.exit("entry.png is not a PNG file")
    if len(blob) > HARD_LIMIT:
        sys.exit("entry.png breaks the 1 MiB gate: %d bytes" % len(blob))
    if len(blob) != PAGE_BYTES:
        sys.exit("entry.png has %d bytes, the page has %d" % (len(blob), PAGE_BYTES))
    if hashlib.sha256(blob).hexdigest() != PAGE_SHA256:
        sys.exit("entry.png hash mismatch — the page on disk is not the drawn page")


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    blob = read_page(folder)
    verify_page(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(blob)
    sys.stderr.write("entry.png delivered: %d bytes -> %s\n" % (len(blob), dest))


if __name__ == "__main__":
    main()
