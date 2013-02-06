About
-----
The scripts in this repo collect data on all the products in a category from newegg.com and store the data into a SQLite database table.


Run a script
------------
As long as the dependencies are installed (lxml, pandas, requests), just run one of the scripts to get the latest data. For example, to get the latest product data for solid state drives simply run:

```bash
python ssd.py
```

A table will be created in the **db/newegg.db** database (if it doesn't already exist) and the latest data will be inserted.


Query the database
------------------
Here is a little snippet that can be used to turn a table in the database into a pandas DataFrame:

```python
import sqlite3
from pandas.io.sql import read_frame

db = sqlite3.connect('db/newegg.db')
micedf = read_frame('SELECT * FROM ssd', db)
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
micedf = data['ssd']
```
