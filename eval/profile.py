#!/usr/bin/env python3
"""Compatibility front-end for profiling the bundled evaluation corpus.

The default corpus is resolved next to this script, never from the caller's cwd.
For the full interface use ``metrics.py profile|compare|aggregate``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

try:  # Works both as ``python eval/profile.py`` and ``python -m eval.profile``.
    from .metrics import DEFAULT_CORPUS, aggregate_corpus, format_aggregate
except ImportError:  # pragma: no cover - exercised by the script-style CLI
    from metrics import DEFAULT_CORPUS, aggregate_corpus, format_aggregate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aggregate the humanizer evaluation corpus (compatibility wrapper)."
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=DEFAULT_CORPUS,
        help=f"corpus directory (default: {DEFAULT_CORPUS})",
    )
    parser.add_argument("--json", action="store_true", help="emit stable JSON")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = aggregate_corpus(args.corpus)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(format_aggregate(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
