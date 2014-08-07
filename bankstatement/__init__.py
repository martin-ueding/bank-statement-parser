#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import csv
import datetime
import os.path
import re

import dateutil.parser
import matplotlib.dates
import matplotlib.pyplot as pl
import numpy as np
import prettytable
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

__docformat__ = 'restructuredtext en'

Base = sqlalchemy.ext.declarative.declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    party = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.Date)
    text = sqlalchemy.Column(sqlalchemy.String)
    amount = sqlalchemy.Column(sqlalchemy.Float)


    store_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stores.id'))
    store = sqlalchemy.orm.relationship("Store", backref=sqlalchemy.orm.backref('expenses'))

    def __repr__(self):
        return 'Expense({party}, {date}, {text}, {amount}, {store})'.format(
            amount=self.amount, date=self.date, party=self.party,
            text=self.text, store=self.store,
        )


class Store(Base):
    __tablename__ = 'stores'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    regex = sqlalchemy.Column(sqlalchemy.String)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
    category = sqlalchemy.orm.relationship("Category", backref=sqlalchemy.orm.backref('stores'))

    def __repr__(self):
        return self.name

    def compile_regex(self):
        self.pattern = re.compile(self.regex)

class Category(Base):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return self.name

def main():
    options = _parse_args()

    engine = sqlalchemy.create_engine('sqlite:///'+options.sqlfile, echo=options.echo_sql)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    Base.metadata.create_all(engine)

    if options.action == 'add':
        if options.what == 'category':
            new_category = Category(name=options.extra[0])
            session.add(new_category)
            session.commit()
        if options.what == 'store':
            name, category_name, regex = options.extra
            category = session.query(Category).filter(Category.name == category_name).scalar()
            if category is None:
                category = Category(name=category_name)
            new_store = Store(name=name, category=category, regex=regex)
            session.add(new_store)
            session.commit()

    elif options.action == 'table':
        if options.what == 'category':
            categories = session.query(Category)
            t = prettytable.PrettyTable(['id', 'name'])
            t.align = 'l'
            t.align['id'] = 'r'
            for category in categories:
                t.add_row([category.id, category.name])
            print(t)
        if options.what == 'store':
            stores = session.query(Store)
            t = prettytable.PrettyTable(['ID', 'Name', 'Category', 'Regex'])
            t.align = 'l'
            t.align['id'] = 'r'
            for store in stores:
                t.add_row([store.id, store.name, store.category.name, store.regex])
            print(t)
        if options.what == 'expense':
            expenses = session.query(Expense).filter(Expense.amount < 0)
            t = prettytable.PrettyTable(['ID', 'Amount', 'Date', 'Party', 'Text', 'Store', 'Category'])
            t.align = 'l'
            t.align['id'] = 'r'
            t.align['amount'] = 'r'
            for expense in expenses:
                t.add_row([expense.id, expense.amount, expense.date,
                           expense.party, expense.text[:20], expense.store,
                           None if expense.store is None else expense.store.category])
            print(t)

    elif options.action == 'delete':
        if options.what == 'store':
            id, = options.extra
            store = session.query(Store).filter(Store.id == id).scalar()
            session.delete(store)
            session.commit()

    elif options.action == 'import':
        with open(options.what) as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:
                # Split up all the columns. Those are the German meanings. Only
                # the ones that are really needed are taken.
                auftragskonto, buchungstag, valutadatum, buchungstext, \
                verwendungszweck, glaeubiger_id, mandatsreferenz, \
                kundenreferenz, sammlerreferenz, lastschrift_ursprungsbetrag, \
                auslagenersatz_ruecklastschrift, beguenstigter, iban, bic, \
                betrag, waehrung, info = row

                e = {}
                e['amount'] = float(betrag.replace(',', '.'))
                e['date'] = dateutil.parser.parse(buchungstag, dayfirst=True)
                e['party'] = re.sub('\s+', ' ', beguenstigter).strip()
                e['text'] = re.sub('\s+', ' ', verwendungszweck).strip()

                result = session.query(Expense).filter(Expense.party == e['party']).filter(Expense.text == e['text']).scalar()

                if result is None:
                    new_expense = Expense(**e)
                    session.add(new_expense)
                    print('Added:', new_expense)
                else:
                    print('Expense already in database.')
        session.commit()

    elif options.action == 'truncate':
        if options.what == 'expense':
            expenses = session.query(Expense)
            for expense in expenses:
                session.delete(expense)
            session.commit()

    elif options.action == 'plot':
        if options.what == 'lines':
            expenses = session.query(Expense).filter(Expense.amount < 0)
            sums = {}
            sums_date = {}
            for expense in expenses:
                year = expense.date.year
                month = expense.date.month
                if expense.store is None:
                    category = 'None'
                else:
                    category = expense.store.category.name
                amount = expense.amount

                date = (year - 2000) + (month-1)/12

                if not category in sums:
                    sums[category] = {}
                if not date in sums[category]:
                    sums[category][date] = 0.0

                if not date in sums_date:
                    sums_date[date] = 0.0

                sums[category][date] -= amount
                sums_date[date] -= amount

            for category, data in sorted(sums.items()):
                l = sorted(list(data.items()))
                dates, amounts = zip(*l)

                pl.plot(dates, amounts, label=category, marker='o')

            l = sorted(list(sums_date.items()))
            dates, amounts = zip(*l)
            pl.plot(dates, amounts, label='Sum', linewidth=2, marker='o', color='black')

            pl.legend(loc='best')
            pl.grid(True)
            pl.title('Monthly spendings grouped by category')
            pl.xlabel('Year ($-2000$)')
            pl.ylabel('€')
            pl.savefig('plot-lines.pdf')
            pl.clf()

    elif options.action == 'csv':
        if options.what == 'months':
            expenses = session.query(Expense).filter(Expense.amount < 0)
            sums = {}
            sums_date = {}
            for expense in expenses:
                year = expense.date.year
                month = expense.date.month
                if expense.store is None:
                    category = 'None'
                else:
                    category = expense.store.category.name
                amount = expense.amount

                date = '{:04d}-{:02d}-01'.format(year, month)

                if not category in sums:
                    sums[category] = {}
                if not date in sums[category]:
                    sums[category][date] = 0.0

                if not date in sums_date:
                    sums_date[date] = 0.0

                sums[category][date] -= amount
                sums_date[date] -= amount

            for category, data in sorted(sums.items()):
                with open('plot-{}.csv'.format(category), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for row in sorted(data.items()):
                        writer.writerow(row)

    sync_all(session)

def sync_all(session):
    '''
    Matches the given stores to all expenses.
    '''
    stores = session.query(Store)
    expenses = session.query(Expense).filter(Expense.store == None)
    for expense in expenses:
        for store in stores:
            matcher = re.search(store.regex, expense.party)
            if matcher:
                expense.store = store

    session.commit()

def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('action', type=str)
    parser.add_argument('what', type=str)
    parser.add_argument('extra', type=str, nargs='*')
    #parser.add_argument('--delimiter', default=';', help='CSV delimiter. Default %(default)s.')
    parser.add_argument('--echo-sql', action='store_true')
    parser.add_argument('--sqlfile', default=os.path.expanduser('~/.local/share/bank-statement-parser/expenses.sqlite'))
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()

if __name__ == '__main__':
    main()
