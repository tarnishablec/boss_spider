# just for test

from pymongo import MongoClient
from pymongo import ReadPreference


class JobReader(object):
    conn = MongoClient(['144.202.33.124:27017', '144.202.33.124:27018', '144.202.33.124:27019'])
    db = conn.get_database('jobs', read_preference=ReadPreference.SECONDARY_PREFERRED)

    def __init__(self, keyword, city):
        self.keyword = keyword
        self.city = city
        self.coll_name = self.keyword + '_' + self.city

    def run(self):
        coll = self.db[self.coll_name]
        results = coll.find({'company_name': '菜鸟网络'})
        print(results)
        for result in results:
            print(result)


def main():
    writer = JobReader('java', '杭州')
    writer.run()


if __name__ == '__main__':
    main()
