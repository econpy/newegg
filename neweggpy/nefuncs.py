from __future__ import division
from ast import literal_eval as le
from datetime import datetime
from json import loads
from lxml.html import fromstring
from math import ceil
from pandas import DataFrame
from time import sleep
import os
import requests
import sqlite3

dtn = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def IterPages(rootobj):
    t = rootobj.cssselect('span.colorGrey')[0].text
    t = filter(lambda x: x.isdigit(), t)
    return int(ceil(int(t)/20))


def BoolToInt(boolobj):
    if boolobj == True:
        return 1
    else:
        assert boolobj == False
        return 0


def getPIDS(urlList, pg1root):
    ProductList = []
    for k, url in enumerate(urlList):
        if k is 0:  # Reuse the root object for the first page
            for el in pg1root.cssselect('a.listCell'):
                ProductList.append(el.attrib['href'])
        else:
            r = requests.get(url).content
            for el in fromstring(r).cssselect('a.listCell'):
                ProductList.append(el.attrib['href'])
    pids = [i.split('=')[1] for i in ProductList if i.count('itemNumber=') == 1]
    return pids


def getData(pidList):
    apiurl = 'http://www.ows.newegg.com/Products.egg'
    OutData = []
    for pid in pidList:
        sleep(1)
        try:
            r = requests.get('%s/%s' % (apiurl, pid)).content
            js = loads(r)
            g = {}
            g['Title'] = js['Title']
            final_price = js['FinalPrice'].replace(',', '')
            if final_price.count('Checkout') == 1:
                g['FinalPrice'] = float('NaN')
            elif final_price == 'See price in cart':
                g['FinalPrice'] = float(js['MappingFinalPrice'].replace(',', '').replace('$', ''))
            else:
                g['FinalPrice'] = float(final_price.replace('$', ''))
            g['OriginalPrice'] = float(js['OriginalPrice'].replace(',', '').replace('$', ''))
            g['Instock'] = BoolToInt(js['Instock'])
            g['Rating'] = js['ReviewSummary']['Rating']
            try:
                g['TotalReviews'] = le(js['ReviewSummary']['TotalReviews'])[0]
            except:
                g['TotalReviews'] = 0
            g['IsHot'] = BoolToInt(js['IsHot'])
            ShippingPrice = js['ShippingInfo']['NormalShippingText'].split(' ')[0]
            if ShippingPrice.count('Free') == 1:
                g['ShippingPrice'] = 0.0
            elif ShippingPrice.count('Special') == 1:
                g['ShippingPrice'] = 2.99   # "Special shipping => $2.99 Egg Saver Shipping"
            else:
                g['ShippingPrice'] = float(ShippingPrice.replace('$', ''))
            g['IsShipByNewegg'] = BoolToInt(js['IsShipByNewegg'])

            if len(js['PromotionText']) > 0:
                g['Promotion'] = js['PromotionText']
            else:
                g['Promotion'] = 'NaN'
            MIR = js['MailInRebateInfo']
            if MIR is None:
                g['MailInRebateInfo'] = 'NaN'
            else:
                g['MailInRebateInfo'] = js['MailInRebateInfo'][0]
            g['PID'] = pid
            g['Brand'] = js['CoremetricsInfo']['Brand']
            g['Date'] = dtn
            OutData.append(g)
        except:
            print 'FAILED: %s' % pid
            pass
    dframe = DataFrame(OutData)
    dframe['FinalPriceShipped'] = dframe['FinalPrice'] + dframe['ShippingPrice']

    return dframe


def insertData(tbl, dframe):
    thisdir = os.path.abspath(os.path.dirname(__file__))
    dbpath = os.path.join(thisdir, '../db/newegg.db')
    
    # CONNECT TO SQLITE DATABASE
    db = sqlite3.connect(dbpath)
    curs = db.cursor()

    # CREATE TABLE IF NEEDED
    tblstr = 'CREATE TABLE IF NOT EXISTS %s (brand TEXT, date TEXT, ' % tbl + \
             'finalprice REAL, instock INTEGER, ishot INTEGER, ' + \
             'isshipbynewegg INTEGER, rebate TEXT, originalprice REAL, pid TEXT, ' + \
             'promotion TEXT, rating INTEGER, shippingprice REAL, title TEXT, ' + \
             'totalreviews INTEGER, finalpriceshipped REAL)'
    curs.execute(tblstr)

    # INSERT ALL THE DATA AT ONCE
    curs.executemany('INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' % tbl,
                      [tuple(i[1]) for i in dframe.iterrows()])
    db.commit()
    curs.close()
    db.close()
