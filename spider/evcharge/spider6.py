import urllib2
import numpy as np
import json
import ast
from random import shuffle
from datetime import datetime
import ast
from time import gmtime, strftime
import time as timelib
import sqlite3

leftextreme = 120.8
rightextreme = 121.9
topextreme = 31.5
bottomextreme = 30.6
interval = 0.01
'''
3 example windows
https://www.evchargeonline.com/site/station/map?operatorIds=&equipmentTypes=&areaIds=&longitude=121.198024&latitude=31.300478&radius=3246&aggregationLevel=14
https://www.evchargeonline.com/site/station/map?operatorIds=&equipmentTypes=&areaIds=&longitude=121.136312&latitude=31.349382&radius=3244&aggregationLevel=14
https://www.evchargeonline.com/site/station/map?operatorIds=&equipmentTypes=&areaIds=&longitude=121.251325&latitude=31.241056&radius=3248&aggregationLevel=14
'''
lng_step = 0.05
lat_step = 0.05
cx = sqlite3.connect("./EVcharge_9.27.db")
cx.text_factory = str  
cu=cx.cursor()   

logdict = {}
#f1 = open("./stationlist.txt",'w')
#f2 = open("./stationinfo.txt",'w')
#f1.write("operatorId,stationId\n")
#f2.write("operatorId,stationId,stationLat,stationLng,address,publicQty,privateQty,totalQty,type(1-private;0-common),status\n")
while(True):
	records=[]
	for lng in np.arange(leftextreme,rightextreme,lng_step):
		for lat in np.arange(bottomextreme,topextreme,lat_step):
			#read station info 
			url = "https://www.evchargeonline.com/site/station/map?operatorIds=&equipmentTypes=&areaIds=&longitude="+str(lng)+"&latitude="+str(lat)+"&radius=3246&aggregationLevel=14"
			flag=True
			while(flag):
				try:
					resp = urllib2.urlopen(url)
					flag=False
				except Exception,e:
					timelib.sleep(10)
					continue
			js_encoded = resp.read()
			js_decoded = json.loads(js_encoded).replace("true","\"true\"")
			station_list = eval(js_decoded)['data']['stations']
			print str(lat)+";"+str(lng)+";"+str(len(station_list))
			for station in station_list:
				opid = station["operatorId"]
				stationId = station["stationId"]
				stid = stationId
				url = "https://www.evchargeonline.com/station/detail/"+opid+"/"+stid+"/1"
				try:
					resp = urllib2.urlopen(url)
				except Exception,e:
					continue
				js_encoded = resp.read()
				js_decoded = json.loads(js_encoded).replace("true","\"true\"").replace(";",",")
				try:
					data = eval(js_decoded)['data']
				except Exception,e:
					print Exception,":",e
					print js_decoded
					continue
				time = str(datetime.now())
				records.append((time,opid,stid,data['parkNums'],data['payment'],data['busineHour'],data['electricityFee'],data['serviceFee'],data['parkFee'],data['directTotal'],data['directAvaliable'],data['alternatingTotal'],data['alternatingAvaliable']))
	cu.executemany("INSERT INTO data VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",records)
	cx.commit()  
