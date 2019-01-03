from pymongo import MongoClient
import spider

conn = MongoClient('104.207.157.182', 27017)

city_name = ''

db_name = 'spider'+city_name

db = conn.db_name



