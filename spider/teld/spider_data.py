#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import sqlite3
import math
import re,random
import sys
import multiprocessing
from datetime import datetime
import json
import time
import urllib2
cx = sqlite3.connect("./teld.db")
cx.text_factory = str  
cu=cx.cursor()   
ids = []
f = open("GetStationNetword.htm")
content = json.load(f)['rows']
for station in content:
	id = station['code']
	ids.append(id)
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
lasttime = 0
while(True):
	currenttime = float(time.time())
	if(currenttime-lasttime>60*40):
		records = []
		lasttime=currenttime
		print str(datetime.now())+" start"
		cnt = -1
		for id in ids:
			cnt+=1
			if(cnt%20==0):
				print str(datetime.now())+" "+str(cnt)
			url = "https://www.teld.cn/StationNetwork/GetChargingStationByCodeList?StationNo="+str(id)
			req = urllib2.Request(url,headers=hdr)
			try:
				page = urllib2.urlopen(req).read()
			except urllib2.HTTPError,e:
				print e.fp.read()
			data = json.loads(page)
			fast_avail = 0
			fast_not_avail = 0
			slow_avail = 0
			slow_not_avail = 0
			for pile in data:	
				if(int(pile['piletype'])>1050):#交流 慢充
					if(pile['stateName']==u"空闲"):
						slow_avail+=1
					else:
						slow_not_avail+=1
				else:#直流 快充
					if(pile['stateName']==u"空闲"):
						fast_avail+=1
					else:
						fast_not_avail+=1
			ctime = str(datetime.now())
			records.append((ctime,id,fast_avail,fast_not_avail,slow_avail,slow_not_avail))
		cu.executemany("INSERT INTO data VALUES(?,?,?,?,?,?)",records)
		cx.commit()  
		print str(datetime.now())+" end"
	time.sleep(20*60)