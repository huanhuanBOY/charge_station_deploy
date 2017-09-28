# -*- coding : utf-8 -*-
import sqlite3

sqlite_connection = sqlite3.connect("/Users/chaidi/Desktop/SHParking.db")

cursor = sqlite_connection.cursor()

select_sql1 = "SELECT DISTINCT crawlTime FROM Park"
insert_sql = "insert into record(crawlTime,countNum) VALUES(?,?)"
count_sql = 'SELECT count(*) from Park where crawlTime = ?'

cursor.execute(select_sql1)

crawlTimes = cursor.fetchall()



for crawlTime in crawlTimes:
    cursor.execute(count_sql, crawlTime)
    count_num = cursor.fetchone()
    cursor.executemany(insert_sql, [(crawlTime[0], count_num[0])])
    sqlite_connection.commit()

cursor.close()