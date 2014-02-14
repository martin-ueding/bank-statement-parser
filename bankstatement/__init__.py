#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import csv
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

class Store(Base):
    __tablename__ = 'stores'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
    category = sqlalchemy.orm.relationship("Category", backref=sqlalchemy.orm.backref('stores'))

class Category(Base):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Category({name}, id={id})'.format(name=self.name, id=self.id)

def main():
    options = _parse_args()

    engine = sqlalchemy.create_engine('sqlite:///test.sqlite', echo=False)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    Base.metadata.create_all(engine)

    if options.action == 'add':
        if options.what == 'category':
            new_category = Category(options.extra[0])
            session.add(new_category)
            session.commit()

    if options.action == 'table':
        if options.what == 'category':
            categories = session.query(Category)
            t = prettytable.PrettyTable(['id', 'name'])
            for category in categories:
                t.add_row([category.id, category.name])
            print(t)

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
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()

if __name__ == '__main__':
    main()
