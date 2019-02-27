# 多线程

import threading
from queue import Queue
import requests
import json
from lxml import etree
import time


class MultiJobShelfSpider:
    ct_list = []
    pt_list = []
    result = []

    def __init__(self, keyword, location):
        self.lock = threading.Lock()
        self.keyword = keyword
        self.location = location
        self.index_queue = Queue()
        self.page_queue = Queue()
        for i in range(1, 11):
            self.index_queue.put(i)

    def run(self):
        self.create_collect_thread()
        self.create_parse_thread()

        for ct in self.ct_list:
            ct.start()
        for pt in self.pt_list:
            pt.start()

        for ct in self.ct_list:
            ct.join()
        for pt in self.pt_list:
            pt.join()

        return self.result

    def create_collect_thread(self):
        collect_name = ['c1', 'c2', 'c3']
        for name in collect_name:
            self.ct_list.append(CollectThread(name, self.index_queue, self.page_queue, self.keyword, self.location))

    def create_parse_thread(self):
        parse_name = ['p1', 'p2', 'p3']
        for name in parse_name:
            self.pt_list.append(ParseThread(name, self.page_queue, self.result, self.lock))


class CollectThread(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.109 Safari/537.36 '
    }
    # url = 'https://www.zhipin.com/c101210100/?query=java&page=1&ka=page-1'
    base_url = 'https://www.zhipin.com'
    city_json_url = 'https://www.zhipin.com/common/data/city.json'
    city_json = requests.get(city_json_url).content

    def __init__(self, name, index_queue, page_queue, keyword, location):
        super(CollectThread, self).__init__()
        self.name = name
        self.index_queue = index_queue
        self.page_queue = page_queue
        self.keyword = keyword
        self.location = location
        self.city_code = self.get_addr_code()

    def run(self):
        print('collect begin')
        while not self.index_queue.empty():
            index = self.index_queue.get()
            full_url = self.joint_url() + str(index) + '&ka=page-' + str(index)
            print(full_url)
            r = requests.get(full_url, headers=self.headers)
            time.sleep(0.05)
            self.page_queue.put(r.content)
        # print('collect over')

    def get_addr_code(self):
        cities = json.loads(self.city_json)
        for city_data in cities['data']['cityList']:
            if city_data['subLevelModelList'] is not None:
                for sub_city_data in city_data['subLevelModelList']:
                    if sub_city_data['name'] == self.location:
                        return sub_city_data['code']
        return 0

    def joint_url(self):
        return self.base_url + '/c' + str(self.city_code) + '/?query=' + self.keyword + '&page='


class ParseThread(threading.Thread):
    def __init__(self, name, page_queue, result, lock):
        super(ParseThread, self).__init__()
        self.name = name
        self.page_queue = page_queue
        self.result = result
        self.lock = lock

    def run(self):
        print("parse begin")
        time.sleep(1)
        while not self.page_queue.empty():
            while not self.page_queue.empty():
                page = self.page_queue.get()
                self.parse_content(page)

    def parse_content(self, page):
        tree = etree.HTML(page)
        job_info_list = tree.xpath('//div[@class="job-primary"]')
        for job in job_info_list:
            job_id = job.xpath('.//div[@class="info-primary"]//a/@data-jobid')[0]
            href = job.xpath('.//div[@class="info-primary"]//a/@href')[0]
            salary = job.xpath('.//div[@class="info-primary"]//span/text()')[0]
            company_name = job.xpath('.//div[@class="company-text"]//h3//a/text()')[0]
            job_title = job.xpath('.//div[@class="info-primary"]//h3//div[@class="job-title"]/text()')[0]
            addr_simple = job.xpath('.//div[@class="info-primary"]//p/text()')[0]
            experience = job.xpath('.//div[@class="info-primary"]//p/text()')[1]
            education = job.xpath('.//div[@class="info-primary"]//p/text()')[2]
            industry = job.xpath('.//div[@class="company-text"]//p/text()')[0]
            # size = job.xpath('.//div[@class="company-text"]//p/text()')[2]
            date = job.xpath('.//div[@class="info-publis"]//p/text()')[0]

            print(job_id)
            print(href)
            print(salary)
            print(company_name)
            print(job_title)
            print(addr_simple)
            print(experience)
            print(education)
            print(industry)
            # print(size)
            print(date)
            print('-------')

            job_data = {
                'job_id': job_id,
                'href': href,
                'job_title': job_title,
                'salary': salary,
                'addr_simple': addr_simple,
                'experience': experience,
                'education': education,
                'company_name': company_name,
                'industry': industry,
                # 'size': size,
                'date': date,
            }
            self.lock.acquire()
            self.result.append(job_data)
            self.lock.release()


def main():
    keyword = 'python'
    city = '南京'

    spider = MultiJobShelfSpider(keyword, city)
    spider.run()


if __name__ == '__main__':
    main()
