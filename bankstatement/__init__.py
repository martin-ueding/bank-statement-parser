#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import csv
import matplotlib.pyplot as pl
import numpy as np
import prettytable

import bankstatement.expense

__docformat__ = 'restructuredtext en'

def main():
    options = _parse_args()

    expenses = []

    for statement in options.statements:
        with open(statement) as f:
            reader = csv.reader(f, delimiter=options.delimiter)
            next(reader)
            for row in reader:
                expenses.append(bankstatement.expense.Expense(*row))

    report_data = []
    t = prettytable.PrettyTable(['Date', 'Category', 'Store', 'Amount'])
    t.align = 'l'
    for expense in expenses:
        if expense.amount < 0 and expense.store.title is not None:
            row = [expense.date, expense.store.category, expense.store.title, '{:+7.2f} €'.format(expense.amount)]
            t.add_row(row)
            report_data.append(expense)
    print(t)

    report_categories(report_data)

def report_categories(expenses):
    total = sum([expense.amount for expense in expenses])
    cs = {}
    for expense in expenses:
        if not expense.store.category in cs:
            cs[expense.store.category] = 0.0
        cs[expense.store.category] += expense.amount

    labels, sub_totals = zip(*cs.items())
    fractions = np.array(sub_totals) / total

    fig = pl.figure(1, figsize=(15,15))
    #ax = fig.axes([0.1, 0.1, 0.8, 0.8])
    ax = fig.add_subplot(1, 1, 1)

    labels = ['{} | {:.2f} € | {:.0f}%'.format(x, y, z*100) for x, y, z in zip(labels, sub_totals, fractions)]

    ax.pie(fractions, labels=labels)
    fig.savefig('report_categories.pdf')

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
