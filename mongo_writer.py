from pymongo import MongoClient
from jobShelfSpider import BossSpider

conn = MongoClient('xxx.xxx.xxx.xxx', 27017)

db_spider = conn.spider

spider = BossSpider('java', '南京', 1, 2)

coll_name = spider.keyword + '_' + spider.city

coll = db_spider[coll_name]

coll.insert_many(spider.run())
