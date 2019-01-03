from pymongo import MongoClient
from spider import BossSpider

conn = MongoClient('104.207.157.182', 27017)

db_spider = conn.spider

spider = BossSpider('java', '南京', 1, 2)

coll_name = spider.city + '_' + spider.keyword

coll = db_spider[coll_name]

coll.insert_many(spider.run())
