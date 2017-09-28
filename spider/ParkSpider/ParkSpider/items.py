# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class ParkSpiderItemloader(ItemLoader):
    default_output_processor = TakeFirst()


class ParkspiderItem(scrapy.Item):

    parkID = scrapy.Field()

    parkName = scrapy.Field()

    address = scrapy.Field()

    areaName = scrapy.Field()

    surplusQuantity = scrapy.Field()

    totalNum = scrapy.Field()

    entLati = scrapy.Field()

    entLongi = scrapy.Field()

    parkType = scrapy.Field()

    fee = scrapy.Field()

    businessTime = scrapy.Field()

    chargeType = scrapy.Field()

    companyName = scrapy.Field()

    hightLimit = scrapy.Field()

    crawlTime = scrapy.Field()

    pass
