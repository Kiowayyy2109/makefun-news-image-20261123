#!/usr/bin/env python3
"""news-image-20261123 entry: write the day's news image to /output/entry.png.

The image (artwork.png, drawn procedurally in the build session) sums up the
world news of Monday 23 November 2026: NATO meets in Brussels after Russian
missiles entered Poland; COP31 collapses with no deal; a drone strike near
Kyiv leaves 14 missing; the search resumes at the Serang factory fire; India
smash a record 720/9 in Wellington; and the Hunger Games roars back at the
box office.

Standard library only, no network, deterministic: this program copies the
bundled artwork byte-for-byte and verifies it with a sha256 self-check, so
both grader runs write identical bytes.
"""

import hashlib
import os
import struct
import sys

EXPECTED_SHA256 = "972de2f0ad189bfad75fd262693292104fb1ff4459fb07c32b0dae75efa9288b"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "artwork.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        print(f"cannot read artwork.png: {exc}", file=sys.stderr)
        return 2

    if not data.startswith(PNG_SIGNATURE):
        print("artwork.png is not a PNG file", file=sys.stderr)
        return 3

    if len(data) < 33 or data[12:16] != b"IHDR":
        print("artwork.png has no IHDR chunk", file=sys.stderr)
        return 3
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"artwork.png is {width}x{height}, expected "
              f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}", file=sys.stderr)
        return 3

    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"artwork.png sha256 mismatch: got {digest}", file=sys.stderr)
        return 4

    if len(data) > 1048576:
        print(f"artwork.png too large: {len(data)} bytes", file=sys.stderr)
        return 5

    os.makedirs(out_dir, exist_ok=True)
    tmp = dst + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, dst)
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
