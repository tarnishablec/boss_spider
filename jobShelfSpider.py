# -*- coding: utf-8 -*-
# 单线程

import urllib.request
import urllib.parse
import re
import json
import requests
import operator
import sys

from bs4 import BeautifulSoup


class JobShelfSpider(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36 '
    }
    # url = 'https://www.zhipin.com/c101210100/?query=java&page=1&ka=page-1'
    url = 'https://www.zhipin.com'
    city_json_url = 'https://www.zhipin.com/common/data/city.json'

    def run(self):
        for page in range(self.start_page, self.end_page + 1):
            request = self.handle_request(page)
            handler = urllib.request.HTTPHandler()
            opener = urllib.request.build_opener(handler)
            content = opener.open(request)
            try:
                self.parse_content(content)
            except IndexError:
                pass
        return self.items

    def __init__(self, keyword, city, start_page=1, end_page=10):
        self.keyword = keyword
        self.city = self.normalize_city(city)
        self.city_code = self.get_addr_code(self.city)
        self.start_page = start_page
        self.end_page = end_page
        self.items = []

    @staticmethod
    def normalize_city(city):
        return re.sub(r'市?\s*', '', city)

    def handle_request(self, page):
        data = {
            'query': self.keyword,
            'page': page,
            'ka': 'page-' + str(page)
        }
        form_data = urllib.parse.urlencode(data)

        if operator.eq(self.city_code, 'bad'):
            print('no such city')
            sys.exit(0)
        else:
            url_now = self.url + '/' + 'c' + str(self.city_code) + '/?' + form_data

        print(url_now)

        request = urllib.request.Request(url=url_now, headers=self.headers)
        return request

    def get_addr_code(self, city):
        resp = requests.get(self.city_json_url)
        city_json = resp.text

        # "code": 101190100, "name": "南京"

        json_loads = json.loads(city_json)

        for city_data in json_loads['data']['cityList']:
            if city_data['subLevelModelList'] is not None:
                for sub_city_data in city_data['subLevelModelList']:
                    if operator.eq(sub_city_data['name'], city):
                        return sub_city_data['code']
        return 'bad'

    def parse_content(self, content):
        soup = BeautifulSoup(content, 'lxml')
        job_soup = soup.select('li > .job-primary')

        # print(job_soup[0])

        pattern1 = re.compile(r'<p>(.+?)<em')
        pattern2 = re.compile(r'</em>(.+?)<em')
        pattern3 = re.compile(r'</em>.+</em>(.+?)</p>')
        pattern4 = re.compile(r'发布于(.+?)</p>')

        # print(job_soup[0])
        for job_info in job_soup:
            job_id = job_info.select('.name > a')[0]['data-jobid']
            href = job_info.select('.name > a')[0]['href']
            job_title = job_info.select('.job-title')[0].text
            salary = job_info.select('span')[0].text
            addr_simple = pattern1.findall(str(job_info))[0]
            experience = pattern2.findall(str(job_info))[0]
            education = pattern3.findall(str(job_info))[0]
            company_name = job_info.select('.company-text > h3 > a')[0].text
            industry = pattern1.findall(str(job_info))[1]
            # size = pattern3.findall(str(job_info))[1]
            date = pattern4.findall(str(job_info))[0]
            job_data = {
                'jobId': job_id,
                'href': href,
                'jobTitle': job_title,
                'salary': salary,
                'addrSimple': addr_simple,
                'experience': experience,
                'education': education,
                'companyName': company_name,
                'industry': industry,
                # 'size': size,
                'date': date,
            }

            self.items.append(job_data)

            # print(href)
            # print(job_id)
            # print(job_title)
            # print(salary)
            # print(addr_simple)
            # print(experience)
            # print(education)
            # print(company_name)
            # print(industry)
            # # print(size)
            # print(date)
            # print('-------')

    def to_json_file(self):
        string = json.dumps(self.items, ensure_ascii=False)
        with open(self.city + '_' + self.keyword + '.json', 'w', encoding='utf-8')as fp:
            fp.write(string)


def main():
    keyword = input('please give a keyword: ')
    city = input('please give a city: ')
    start_page = 1
    end_page = 10

    spider = BossSpider(keyword, city, start_page, end_page)
    spider.to_json_file()


if __name__ == '__main__':
    main()
