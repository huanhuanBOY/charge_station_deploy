# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import socket
import pymysql.cursors
from twisted.enterprise import adbapi
import sqlite3

class ParkspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ParkSpiderMySqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        hostName = socket.getfqdn(socket.gethostname())
        hostIp = socket.gethostbyname(hostName)
        dbparms = dict(
            host = str(hostIp),
            user = settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            db = settings["MYSQL_DBNAME"],
            charset = 'utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item)
        return item

    def handle_error(self, failure, item):
        print(failure)

    def do_insert(self, cursor, item):
        sql = """
                      INSERT INTO Park1(
                      parkID,
                      parkName,
                      address,
                      areaName,
                      crawlTime,
                      surplusQuantity,
                      totalNum,
                      entLati,
                      entLongi,
                      parkType,
                      fee,
                      businessTime,
                      chargeType,
                      companyName,
                      hightLimit
                      ) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                      """
        cursor.execute(sql, (item["parkID"],
                             item["parkName"],
                             item["address"],
                             item["areaName"],
                             item["crawlTime"],
                             item["surplusQuantity"],
                             item["totalNum"],
                             item["entLati"],
                             item["entLongi"],
                             item["parkType"],
                             item["fee"],
                             item["businessTime"],
                             item["chargeType"],
                             item["companyName"],
                             item["hightLimit"]
                             ))
        return item


class ParkSpiderSqlatePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("sqlite3", '/Users/chaidi/Documents/sqlite-snapshot-201708251543/SHParking.db',
                                            check_same_thread=False)
        pass

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item)
        return item

    def handle_error(self, failure, item):
        print(failure)

    def do_insert(self, cursor, item):
        sql = """
                      INSERT INTO Park(
                      parkID,
                      parkName,
                      address,
                      areaName,
                      crawlTime,
                      surplusQuantity,
                      totalNum,
                      entLati,
                      entLongi,
                      parkType,
                      fee,
                      businessTime,
                      chargeType,
                      companyName,
                      hightLimit
                      ) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """
        cursor.executemany(sql, [(item["parkID"],
                             item["parkName"],
                             item["address"],
                             item["areaName"],
                             item["crawlTime"],
                             item["surplusQuantity"],
                             item["totalNum"],
                             item["entLati"],
                             item["entLongi"],
                             item["parkType"],
                             item["fee"],
                             item["businessTime"],
                             item["chargeType"],
                             item["companyName"],
                             item["hightLimit"],
                             )])
        return item
