#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import csv
import matplotlib.pyplot as pl
import numpy as np
import prettytable

__docformat__ = 'restructuredtext en'

def main():
    options = _parse_args()


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('action', type=str)
    parser.add_argument('what', type=str)
    #parser.add_argument('--delimiter', default=';', help='CSV delimiter. Default %(default)s.')
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()

if __name__ == '__main__':
    main()
