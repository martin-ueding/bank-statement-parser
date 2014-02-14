#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import csv
import dateutil.parser
import matplotlib.pyplot as pl
import numpy as np
import prettytable
import re
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

    def __repr__(self):
        return 'Expense({party}, {date}, {text}, {amount})'.format(
            amount=self.amount, date=self.date, party=self.party,
            text=self.text,
        )


class Store(Base):
    __tablename__ = 'stores'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    regex = sqlalchemy.Column(sqlalchemy.String)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
    category = sqlalchemy.orm.relationship("Category", backref=sqlalchemy.orm.backref('stores'))

class Category(Base):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return 'Category({name}, id={id})'.format(name=self.name, id=self.id)

def main():
    options = _parse_args()

    engine = sqlalchemy.create_engine('sqlite:///test.sqlite', echo=options.echo_sql)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    Base.metadata.create_all(engine)

    if options.action == 'add':
        if options.what == 'category':
            new_category = Category(name=options.extra[0])
            session.add(new_category)
            session.commit()
        if options.what == 'store':
            name, category_name, regex = options.extra
            results = session.query(Category).filter(Category.name == category_name)
            if len(list(results)) == 0:
                category = Category(name=category_name)
            else:
                category = next(results)
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
            t = prettytable.PrettyTable(['id', 'name', 'category', 'regex'])
            t.align = 'l'
            t.align['id'] = 'r'
            for store in stores:
                t.add_row([store.id, store.name, store.category, store.regex])
            print(t)
        if options.what == 'expense':
            expenses = session.query(Expense)
            t = prettytable.PrettyTable(['id', 'amount', 'date', 'party', 'text'])
            t.align = 'l'
            t.align['id'] = 'r'
            t.align['amount'] = 'r'
            for expense in expenses:
                t.add_row([expense.id, expense.amount, expense.date, expense.party, expense.text])
            print(t)

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
                e['date'] = dateutil.parser.parse(buchungstag)
                e['party'] = re.sub('\s+', ' ', beguenstigter).strip()
                e['text'] = re.sub('\s+', ' ', verwendungszweck).strip()

                #print(e)

                result = session.query(Expense).filter(Expense.party == e['party']).filter(Expense.text == e['text']).scalar()

                if result is None:
                    new_expense = Expense(**e)
                    session.add(new_expense)
                    print('Added:', new_expense)
                else:
                    print('Expense already in database.')
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
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()

if __name__ == '__main__':
    main()
