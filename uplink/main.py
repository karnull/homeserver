"""
Copyright (c) 2026 Apache-2.0 license

@file
@author karsh
@brief  Main file
"""


# ==============================================================================
# Imports

from __future__ import annotations

import argparse
import logging
import sys
import time
from typing import Sequence

import colorlog

LOG = logging.getLogger(__name__)


# ==============================================================================
# Helper Functions


def _build_parser(prog: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="A narrow REST server that lets the judy container act on the host",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (repeat: -v, -vv).",
    )
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Reduce output (warnings/errors only).",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
        default=None,
        help="Explicit log level (overrides -v/-q).",
    )

    parser.add_argument(
        "--log-file",
        default=None,
        help="Optional path to a log file.",
    )

    # TODO Example project arg (remove/replace as needed)
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Optional input (example positional argument).",
    )

    return parser


def _resolve_log_level(args: argparse.Namespace) -> int:
    """Derive log level from args with sane precedence."""

    if args.log_level:
        return getattr(logging, args.log_level)

    if args.quiet:
        return logging.WARN

    # default INFO, -vv => DEBUG
    if args.verbose >= 2:
        return logging.DEBUG
    return logging.INFO


def _configure_logging(level: int, log_file: str | None) -> None:
    """
    Configure root logging.

    Uses colorlog when stderr is a TTY; otherwise uses plain formatter
    to avoid ANSI escape codes in redirected output.
    """

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    is_tty = hasattr(sys.stderr, "isatty") and sys.stderr.isatty()
    stream_handler = logging.StreamHandler(sys.stderr)

    if is_tty:
        formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s%(levelname)s%(reset)s\t%(asctime)s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARN": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    else:
        formatter = logging.Formatter(
            fmt="%(levelname)s\t%(asctime)s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )

    stream_handler.setFormatter(formatter)
    root.addHandler(stream_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(levelname)s\t%(asctime)s %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        root.addHandler(file_handler)


# ==============================================================================
# Program Start Point


def run(args: argparse.Namespace) -> int:
    """
    Put your actual app logic here.
    """

    LOG.debug("Arguments: %s", args)

    if args.input:
        LOG.info("Got input: %s", args.input)
    else:
        LOG.info("No input provided.")

    # TODO add code...

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    start = time.perf_counter()

    # Use module name as a sensible default program name.
    prog = (sys.argv[0].rsplit("/", 1)[-1] or "app") if argv is None else "app"

    parser = _build_parser(prog=prog)

    # Inject version from package if available
    try:
        from . import __version__  # type: ignore

        parser.set_defaults(_version=__version__)
        parser._defaults["version"] = __version__  # for action="version"
        parser.version = __version__  # best-effort for some argparse behaviors
        parser.add_argument(
            "--_internal_version", action="store_true", help=argparse.SUPPRESS
        )
        # Note: argparse's "version" action uses `version=` at add_argument time.
        # We keep a simple approach: leave __init__.__version__ for external access.
    except Exception:
        pass

    args = parser.parse_args(argv)

    level = _resolve_log_level(args)
    _configure_logging(level=level, log_file=args.log_file)

    try:
        code = run(args)
        return int(code) if code is not None else 0

    except KeyboardInterrupt:
        LOG.warning("Interrupted by user (Ctrl+C).")
        return 130  # conventional SIGINT exit code

    except Exception:
        LOG.exception("Unhandled exception")
        return 1

    finally:
        elapsed = time.perf_counter() - start
        LOG.debug("Elapsed: %.3fs", elapsed)


if __name__ == "__main__":
    raise SystemExit(main())
