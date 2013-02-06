import lxml.html
import requests
from neweggpy.nefuncs import IterPages,BoolToInt,getPIDS,getData,insertData

baseurl = 'http://m.newegg.com/ProductList?description=Processors+-+' + \
          'Desktops&categoryId=343&storeId=1&nodeId=7671&' + \
          'parentCategoryId=34&isSubCategory=true&categoryType=1'

pg1 = requests.get(baseurl).content
root1 = lxml.html.fromstring(pg1)
page_count = IterPages(root1)
URLs = ['%s&Page=%s' % (baseurl, pgnum) for pgnum in range(1, page_count + 1)]

# FETCH AND PARSE THE DATA
pids = getPIDS(URLs, root1)
df = getData(pids)

# PUT DATA IN DATABASE
insertData('cpus', df)
