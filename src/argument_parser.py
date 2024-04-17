#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def init_parser():
    parser = argparse.ArgumentParser(description="OSINT information crawler.")
    parser.add_argument("-n", "--name", type=str, help="Name of the person", required=False)
    parser.add_argument(
        "-e", "--entity", type=str, help="Organization, or company name", required=True
    )
    parser.add_argument("-o", "--output", type=str, help="Output file", required=False)
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Increase output verbosity"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")

    return parser
