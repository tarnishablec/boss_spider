from pymongo import MongoClient
from spider import BossSpider

conn = MongoClient('104.207.157.182', 27017)

db_spider = conn.spider

spider = BossSpider('java', '南京', 1, 2)

coll = db_spider.南京_java

coll.insert_many(spider.run())
