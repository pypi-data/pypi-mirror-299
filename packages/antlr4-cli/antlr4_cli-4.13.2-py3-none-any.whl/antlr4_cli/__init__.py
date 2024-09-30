# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import os
import subprocess
import sys
from pathlib import Path

__version__ = "4.13.2"


def _process_args():
    parser = argparse.ArgumentParser(add_help=False, usage="%(prog)s [%(prog)s options]")
    _, unparsed_args = parser.parse_known_args()
    return unparsed_args


def _run_cli(entrypoint):
    args = _process_args()
    jar_file = Path(__file__).parent / f"antlr4-{__version__}"
    cp = subprocess.run(["java", "-cp", jar_file, entrypoint] + args)
    sys.exit(cp.returncode)


def tool():
    """Entry point to run antlr4 tool itself"""
    _run_cli("org.antlr.v4.Tool")


def interp():
    """Entry point to run antlr4 profiling using grammar and input file"""
    _run_cli("org.antlr.v4.gui.Interpreter")
