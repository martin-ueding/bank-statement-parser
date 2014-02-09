#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import csv
import re

__docformat__ = 'restructuredtext en'

class Expense(object):
    def __init__(self, auftragskonto, buchungstag, valutadatum, buchungstext,
                 verwendungszweck, glaeubiger_id, mandatsreferenz,
                 kundenreferenz, sammlerreferenz, lastschrift_ursprungsbetrag,
                 auslagenersatz_ruecklastschrift, beguenstigster, iban, bic,
                 betrag, waehrung, info):
        self.store = Store(beguenstigster)
        self.amount = float(betrag.replace(',', '.'))

    def __repr__(self):
        return '{:-7.2f} {}'.format(self.amount, self.store)

regexes = {
    'ALDI': r'ALDI Sued sagt danke',
    'REWE': r'REWE sagt danke',
    'Kaisers': r'Kaisers Tengelmann',
    'Obi': r'Obi sagt danke',
    'Netto': r'Netto-einfach besser',
    'Alnatura': r'Alnatura dankt',
    'Sparkasse KölnBonn': r'Sparkasse KoelnBonn',
    'SB Möbel Boss': r'BOSS .+ Bornheim',
    'Porta': r'Porta .+ Bornheim',
    'Axel Reiß': r'Axel Reiss',
    'Knauber': r'Knauber',
    'DM': r'DM Drogeriemarkt sagt danke',
    'Geldautomat': r'GA NR\d+ BLZ\d+',
}

for store, regex in regexes.items():
    regexes[store] = re.compile(regex, flags=re.IGNORECASE)

class Store(object):
    def __init__(self, text):
        for store, regex in regexes.items():
            m = regex.search(text)
            if m:
                self.text = store
                return

        self.text = 'unmatched({})'.format(text)

    def __repr__(self):
        return self.text

def main():
    options = _parse_args()

    expenses = []

    for statement in options.statements:
        with open(statement) as f:
            reader = csv.reader(f, delimiter=options.delimiter)
            next(reader)
            for row in reader:
                expenses.append(Expense(*row))

    for expense in expenses:
        print(expense)


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('statements', metavar='statement.csv', type=str, nargs='+', help='Bank statements in CSV CAMT format.')
    parser.add_argument('--delimiter', default=';', help='CSV delimiter. Default %(default)s.')
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()


if __name__ == '__main__':
    main()
