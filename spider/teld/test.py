#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import urllib2

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
url = "https://www.teld.cn/StationNetwork/GetChargingStationByCodeList?StationNo=7e55168a-2bbd-49f7-9377-5e1139064b4c"
req = urllib2.Request(url,headers=hdr)
page = urllib2.urlopen(req).read()
data = json.loads(page)[0]['name']
s = u"直流"
print data[-2:]==s
print data[-2:]
