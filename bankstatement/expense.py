#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import re
import dateutil.parser

__docformat__ = "restructuredtext en"

regexes = {
    'food': {
        'ALDI': r'ALDI Sued sagt danke',
        'REWE': r'REWE sagt danke',
        'Kaisers': r'Kaisers Tengelmann',
        'Netto': r'Netto-einfach besser',
        'Alnatura': r'Alnatura dankt',
    },
    'hardware store': {
        'Obi': r'Obi sagt danke',
        'Knauber': r'Knauber',
    },
    'furniture': {
        'SB Möbel Boss': r'BOSS .+ Bornheim',
        'Porta': r'Porta .+ Bornheim',
    },
    'rent': {
        'Axel Reiß': r'Axel Reiss',
    },
    'hygiene': {
        'DM': r'DM Drogeriemarkt sagt danke',
    },
    'other': {
        'Sparkasse KölnBonn': r'Sparkasse KoelnBonn',
        'Geldautomat': r'GA NR\d+ BLZ\d+',
    },
}

for category, stores in regexes.items():
    for store, regex in stores.items():
        regexes[category][store] = re.compile(regex, flags=re.IGNORECASE)

class Expense(object):
    def __init__(self, auftragskonto, buchungstag, valutadatum, buchungstext,
                 verwendungszweck, glaeubiger_id, mandatsreferenz,
                 kundenreferenz, sammlerreferenz, lastschrift_ursprungsbetrag,
                 auslagenersatz_ruecklastschrift, beguenstigster, iban, bic,
                 betrag, waehrung, info):
        self.store = Store(beguenstigster)
        self.amount = float(betrag.replace(',', '.'))
        self.date = dateutil.parser.parse(buchungstag).date()

    def __repr__(self):
        return '{:-7.2f} {}'.format(self.amount, self.store)

class Store(object):
    def __init__(self, text):
        for category, stores in regexes.items():
            for store, regex in stores.items():
                m = regex.search(text)
                if m:
                    self.title = store
                    self.category = category
                    return

        self.title = None
        self.category = None

    def __repr__(self):
        return '{} {}'.format(self.category, self.text)
