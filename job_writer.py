from pymongo import MongoClient
from jobListSpider import BossSpider


class JobWriter(object):
    conn = MongoClient(['144.202.33.124:27017', '144.202.33.124:27018', '144.202.33.124:27019'])
    db = conn.get_database('jobs')

    def __init__(self, keyword, city):
        self.keyword = keyword
        self.city = city
        self.coll_name = self.keyword + '_' + self.city

    def run(self):
        coll = self.db[self.coll_name]
        spider = BossSpider(self.keyword, self.city)
        coll.insert_many(spider.run())


def main():
    writer = JobWriter('java', '南京')
    writer.run()


if __name__ == '__main__':
    main()
