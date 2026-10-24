"""
Copyright (c) 2026 Apache-2.0 license

@file
@author karsh
@brief  Tests for the command-line options
"""

import logging

from uplink.main import _build_parser, _resolve_log_level


def test_logs_at_info_by_default():
    args = _build_parser("app").parse_args([])
    assert _resolve_log_level(args) == logging.INFO


def test_double_verbose_logs_at_debug():
    args = _build_parser("app").parse_args(["-vv"])
    assert _resolve_log_level(args) == logging.DEBUG


def test_quiet_logs_warnings_only():
    args = _build_parser("app").parse_args(["-q"])
    assert _resolve_log_level(args) == logging.WARN
