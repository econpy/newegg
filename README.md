About
-----
The scripts in this repo collect data on all the products in a category from newegg.com and store the data into a SQLite database table.


Dependencies
-----------
First make sure the following dependencies are installed:

*   [lxml][lxmlgithub]
*   [pandas][pandasgithub]
*   [requests][requestsgithub]


Run a script
-----------
As an example, to get the latest product data for solid state drives simply run:

```bash
python ssd.py
```

That's it! A table will be created in the **db/newegg.db** database (if it doesn't already exist) and the latest data will be inserted.


Query the database
----------------
Here is a little snippet that can be used to turn a table in the database into a pandas DataFrame:

```python
import sqlite3
from pandas.io.sql import read_frame

db = sqlite3.connect('db/newegg.db')
ssd_df = read_frame('SELECT * FROM ssd', db)
```

Or make a dict of DataFrames with keys equal to the table names and values equal to the table as a DataFrame:
```python
import sqlite3
from pandas.io.sql import read_frame

db = sqlite3.connect('db/newegg.db')
tbls = read_frame('SELECT name FROM sqlite_master WHERE type="table"', db)
data = {tbl: read_frame('SELECT * FROM %s' % tbl, db) for tbl in tbls['name']}
```

Then you can get the same DataFrame of solid state drive data as before by doing:
```python
ssd_df = data['ssd']
```

[lxmlgithub]: http://github.com/lxml/lxml
[pandasgithub]: http://github.com/pydata/pandas
[requestsgithub]: http://github.com/kennethreitz/requests
