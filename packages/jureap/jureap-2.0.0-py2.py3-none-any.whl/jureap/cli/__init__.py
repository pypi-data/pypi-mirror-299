# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------

import sys
import os
import argparse
import jureap


def make_wide(formatter, w=140, h=100):
    """Return a wider HelpFormatter, if possible."""
    try:
        # https://stackoverflow.com/a/5464440
        # beware: "Only the name of this class is considered a public API."
        kwargs = {"width": w, "max_help_position": h}
        formatter(None, **kwargs)
        return lambda prog: formatter(prog, **kwargs)
    except TypeError:
        warnings.warn("argparse help formatter failed, falling back.")
        return formatter


def log_parser(sp):
    sp.add_argument(
            "--version",
            type=jureap.metadata.major_version_type,
            default=jureap.metadata.semver.major,
            choices=list(jureap.metadata.major_version_type),
            help="Version of Input File",
            )
    sp.add_argument(
            "--output-version",
            type=jureap.metadata.major_version_type,
            default=jureap.metadata.semver.major,
            choices=list(jureap.metadata.major_version_type),
            help="Version of Log File",
            )
    sp.add_argument("input_file", type=str, help="Input File")
    sp.add_argument("output_file", type=str, help="Output File")


def report_parser(sp):
    pass

def check_parser(sp):
    sp.add_argument("input_file", type=str, help="Result File")


def top_level():
    parser = argparse.ArgumentParser(
            description="jureap",
            formatter_class=make_wide(argparse.ArgumentDefaultsHelpFormatter),
            )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    lp = subparsers.add_parser(
            "log",
            help="Log Generator",
            formatter_class=make_wide(argparse.ArgumentDefaultsHelpFormatter),
            )
    rp = subparsers.add_parser("report", help="Report Generator")

    vp = subparsers.add_parser("check", help="check Result File")

    log_parser(lp)
    check_parser(vp)


    return parser

def main():
    try:
        raw_args = sys.argv[1:]
        parser = top_level()
        args = parser.parse_args(raw_args)

        if args.subcommand == "check":
            input_filename = args.input_file
            jureap.check.check(input_filename)
        else:
            print("Usage Error: Subcommand " + args.subcommand + " not implemented yet.")
            exit(os.EX_USAGE)
    except Exception as e:
        print("Data Error: " + str(e))
        exit(os.EX_DATAERR)


    exit(os.EX_OK)
