..  Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

######################
Command line interface
######################

The syntax is about like so::

    bank-statement-parser action what? [more options] [filters]

Actions
=======

So let us look at the available actions:

table
-----

This will go to the database and fetch some data and print it in an ASCII
table. You can specify the following ``what?``:

categories
    This will list all the categories stored in the database.

stores
    This will list all the stores.

expenses
    List all the expenses.

.. vim: spell tw=79
