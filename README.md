About
-----
Each of these scripts collect data on all the products in a category from newegg.com and store the data in a SQLite database table.

Run a script
------------
As long as the dependencies are installed (lxml, pandas, requests), simply do the following to collect data on all the computer mice:

```bash
git clone git://github.com/econpy/newegg
cd newegg
python mice.py
```

A table will be created in the **db/newegg.db** database (if it doesn't already exist) and the latest data will be inserted.

Query the database
------------------
Here is a little snippet that can be used to turn a table in the database into a pandas DataFrame:

```python
import sqlite3
from pandas.io.sql import read_frame

db = sqlite3.connect('db/newegg.db')
micedf = read_frame('SELECT * FROM mice', db)
```

Or make a dict of DataFrames with keys equal to the table names and values equal to the table as a DataFrame:
```python
import sqlite3
from pandas.io.sql import read_frame

db = sqlite3.connect('db/newegg.db')
tbls = read_frame('SELECT name FROM sqlite_master WHERE type="table"', db)
data = {tbl: read_frame('SELECT * FROM %s' % tbl, db) for tbl in tbls['name']}
```

Then you can get the same mice DataFrame as before by doing:
```python
micedf = data['mice']
```
