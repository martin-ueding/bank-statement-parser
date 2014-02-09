#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import csv

__docformat__ = "restructuredtext en"

def main():
    options = _parse_args()

    for statement in options.statements:
        with open(statement) as f:
            reader = csv.reader(f, delimiter=options.delimiter)
            for row in reader:
                print(row)


def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("statements", metavar="statement.csv", type=str, nargs="+", help="Bank statements in CSV CAMT format.")
    parser.add_argument("--delimiter", default=';', help='CSV delimiter. Default %(default)s.')
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()


if __name__ == "__main__":
    main()
