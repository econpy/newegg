ABOUT
=====
Each of these scripts collect data on all the products in a category from newegg.com and store the data in a SQLite database table.

EXAMPLE
======
As long as you have the dependencies installed (lxml, pandas, requests), simply do the following to collect data on all the computer mice:

'''
git clone git://github.com/econpy/newegg
cd newegg
python mice.py
'''

A table will be created in the db/newegg.db database (if it doesn't already exist) and the latest data will be inserted into the mice table.
