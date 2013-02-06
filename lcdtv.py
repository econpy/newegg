import lxml.html
import requests
from neweggpy.nefuncs import IterPages,BoolToInt,getPIDS,getData,insertData

baseurl = 'http://m.newegg.com/ProductList?description=LCD+TV&categoryId=411' + \
          '&storeId=10&nodeId=7719&parentCategoryId=264&isSubCategory=true&' + \
          'categoryType=1'

pg1 = requests.get(baseurl).content
root1 = lxml.html.fromstring(pg1)
page_count = IterPages(root1)
URLs = ['%s&Page=%s' % (baseurl, pgnum) for pgnum in range(1, page_count + 1)]

# FETCH AND PARSE THE DATA
pids = getPIDS(URLs, root1)
df = getData(pids)

# PUT DATA IN DATABASE
insertData('lcdtv', df)
