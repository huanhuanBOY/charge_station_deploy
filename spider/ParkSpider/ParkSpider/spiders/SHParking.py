# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from ParkSpider.items import ParkspiderItem
from ParkSpider.items import ParkSpiderItemloader

class ShparkingSpider(scrapy.Spider):
    name = 'SHParking'
    allowed_domains = ['http://220.248.75.39:12900/']
    search_radius = 100000
    start_urls = ['http://220.248.75.39:12900/handapp_pms/nearby?latitude=31.23271&longitude=121.506178&'
                  'nearby={}&sysType=IOS&sysCode=10.2&uuId=353B0829-434C-4B7F-A729-8389A574B95D&appVer=1.5.1&'
                  'model=iPhone&parkType=0'.format(search_radius)]

    def return_json_data(self, value):
        return value if value else '-1'

    def parse(self, response):
        crawlTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parkJsons = json.loads(response.text)
        with open('./jsonFile/park_data_{}.json'.format(crawlTime), 'w') as f:
            json.dump(parkJsons, f)
        for parkJson in parkJsons:
            parkItme = ParkspiderItem()
            parkItemLoader = ParkSpiderItemloader(item=parkItme, response=response)
            try:
                parkItemLoader.add_value("parkID", self.return_json_data(parkJson["parkid"]))
                parkItemLoader.add_value("parkName", self.return_json_data(parkJson["parkname"]))
                parkItemLoader.add_value("address", self.return_json_data(parkJson["address"]))
                parkItemLoader.add_value("areaName", self.return_json_data(parkJson["areaName"]))
                parkItemLoader.add_value("crawlTime", self.return_json_data(crawlTime))
                parkItemLoader.add_value("surplusQuantity", self.return_json_data(parkJson["surplusQuantity"]))
                parkItemLoader.add_value("totalNum", self.return_json_data(parkJson["totalNum"]))
                parkItemLoader.add_value("entLati", self.return_json_data(parkJson["entLati"]))
                parkItemLoader.add_value("entLongi", self.return_json_data(parkJson["entLongi"]))
                parkItemLoader.add_value("parkType", self.return_json_data(parkJson["typeName"]))
                parkItemLoader.add_value("fee", self.return_json_data(parkJson["fee"]))
                parkItemLoader.add_value("businessTime", self.return_json_data(parkJson["bussinessTime"]))
                parkItemLoader.add_value("chargeType", self.return_json_data(parkJson["chargeTypeString"]))
                parkItemLoader.add_value("companyName", self.return_json_data(parkJson["companyName"]))
                parkItemLoader.add_value("hightLimit", self.return_json_data(parkJson["hightLimit"]))
                parkItme = parkItemLoader.load_item()
                yield parkItme
            except:
                print("JSONDATAERROR")
