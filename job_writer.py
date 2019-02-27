from pymongo import MongoClient
from bossShelfSpiderMulti import MultiJobShelfSpider


class JobWriter(object):
    conn = MongoClient(['104.238.136.245:27017', '104.238.136.245:27018', '104.238.136.245:27019'])
    db = conn.get_database('boss_job_shelf')

    def __init__(self, keyword, city):
        self.keyword = keyword
        self.city = city
        self.coll_name = self.keyword + '_' + self.city

    def run(self):
        coll = self.db[self.coll_name]
        spider = MultiJobShelfSpider(self.keyword, self.city)
        coll.insert_many(spider.run())


def main():
    writer = JobWriter('java', '杭州')
    writer.run()


if __name__ == '__main__':
    main()
