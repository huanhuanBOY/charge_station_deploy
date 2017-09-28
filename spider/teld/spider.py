#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
from datetime import datetime
import json
import urllib
import time
import urllib2

cx = sqlite3.connect("./teld.db")
cx.text_factory = str  
cu=cx.cursor()   
ids = []

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
lastTime_overview = -1
lastTime_detail = -1
province_detail_list = ['上海市']

def readURLjson(url):
	jsonstr = urllib2.urlopen(urllib2.Request(url, headers=hdr))
	jsonstr = jsonstr.read()
	content = json.loads(jsonstr)
	return content

while(True):
	currentTime = datetime.now()
	time_str = str(currentTime)
	if(lastTime_overview!=currentTime.date()):
		lastTime_overview = currentTime.date()
		#crawl static data every day
		#province
		print datetime.now(),"crawling province overview"
		province_record=[]
		province_url = 'https://www.teld.cn/StationNetwork/GetCityInfoAZ'
		province_content = readURLjson(province_url)
		for k in province_content.keys():
			for pro_js in province_content[k]:
				pro_name = pro_js['Name']
				idxurl = "https://www.teld.cn/StationNetwork/GetStationNetword?ProvinceName="+urllib.quote(pro_name.encode('utf-8'))+"&rows=2000"
				pro_total = readURLjson(idxurl)['total']
				province_record.append((pro_name,time_str,pro_total))
		cu.executemany("insert into province_static values(?,?,?)",province_record)
		cx.commit()
		#station static list
		print datetime.now(),"crawling station list"
		for pro_name in province_detail_list:
			idxurl = "https://www.teld.cn/StationNetwork/GetStationNetword?ProvinceName="+urllib.quote(pro_name)+"&rows=2000"
			detail = readURLjson(idxurl)['rows']
			detail_record = []
			for st in detail:
				#{"code":"7e55168a-2bbd-49f7-9377-5e1139064b4c","name":"上海东淮海国际大厦充电站","longitude":"121.488799","latitude":"31.232033","businessDistrict":null,"fastPileCount":1,"slowPileCount":2,"FreeTerminalNum":3,"operateTypeCode":"3","operateTypeName":"运营中","address":"上海市市辖区黄浦区淮海东路49号","statype":null,"statypename":null}
				id = st['code']
				name = st['name']
				lng = st['longitude']
				lat = st['latitude']
				address = st['address']
				detail_record.append((id,name,lat,lng,address))
			cu.executemany("insert or ignore into station_static values(?,?,?,?,?)",detail_record)
			cx.commit()

	if(lastTime_detail==-1 or (currentTime-lastTime_detail).seconds>60*30):
		lastTime_detail = currentTime
		#crawl dynamic data every half hour
		#station dynamic
		print datetime.now(),"crawling station dynamic"
		for pro_name in province_detail_list:
			idxurl = "https://www.teld.cn/StationNetwork/GetStationNetword?ProvinceName=" + urllib.quote(pro_name) + "&rows=2000"
			detail = readURLjson(idxurl)['rows']
			detail_record = []
			for st in detail:
				#{"code":"7e55168a-2bbd-49f7-9377-5e1139064b4c","name":"上海东淮海国际大厦充电站","longitude":"121.488799","latitude":"31.232033","businessDistrict":null,"fastPileCount":1,"slowPileCount":2,"FreeTerminalNum":3,"operateTypeCode":"3","operateTypeName":"运营中","address":"上海市市辖区黄浦区淮海东路49号","statype":null,"statypename":null}
				id = st['code']
				fastpile = st['fastPileCount']
				slowpile = st['slowPileCount']
				free = st['FreeTerminalNum']
				detail_record.append((id,time_str,fastpile,slowpile,free))
			cu.executemany("insert into station_dynamic values(?,?,?,?,?)",detail_record)
			cx.commit()
		#charger dynamic
		print datetime.now(),"crawling charger dynamic"
		idlist = map(lambda x:x[0],detail_record)
		c_records = []
		for stid in idlist:
			sturl = 'https://www.teld.cn/StationNetwork/GetChargingStationByCodeList?StationNo='+urllib.quote(stid.encode('utf-8'))
			cdetail = readURLjson(sturl)
			for charger in cdetail:
				#{"state":"02","stateName":"空闲","code":"3101040001109","name":"109号直流","piletype":"1001"}
				cid = charger['code']
				name = charger['name']
				type = charger['piletype']
				state = charger['stateName']
				c_records.append((cid,stid,time_str,name,state,type))
		cu.executemany("insert into charger_dynamic values(?,?,?,?,?,?)",c_records)
		cx.commit()
	time.sleep(10*60)

