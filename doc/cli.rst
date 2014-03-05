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

category
    This will list all the categories stored in the database.

store
    This will list all the stores.

expense
    List all the expenses.

add
---

category::

    add category CATEGORY

store::

    add store NAME CATEGORY REGEX

delete
------

::

    delete store STORE

import
------

::

    import FILE.CSV

truncate
--------

::

    truncate expense

plot
----

::
    
    plot lines
    

.. vim: spell tw=79
