# -*- coding:utf-8 -*-
import random
import urllib2
import re
import os

# Define constants
DEFAULT_NUM = 200
MAX_NUM = 2000
MAX_INDEX = 30000


class Spider:
    def __init__(self, number=DEFAULT_NUM):
        max_num = MAX_NUM

        self.num = DEFAULT_NUM
        if type(number) == int and 0 < number <= max_num:
            self.num = number

        self.begin = random.randint(0, MAX_INDEX)

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        self.headers = {"Accept-Language": "zh-CN,zh;q=0.8", 'User-Agent': self.user_agent}

    def get_page(self, url):
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            page_code = response.read()
            return page_code
        except urllib2.URLError:
            return None

    def get_json(self, web_index):
        page_dom = self.get_page("http://www.xiachufang.com/recipe/" + web_index)
        if not page_dom:
            return None

        pattern = re.compile('.*?"application/ld\+json">(.*?)</script>', re.S)
        page_data = re.findall(pattern, page_dom)[0].strip()
        return page_data

    @staticmethod
    def get_web_index(index):
        string = str(index)
        length = len(string)
        while length < 5:
            string = '0' + string
            length += 1
        return string

    def start(self):
        if not os.path.exists(".\\data"):
            os.makedirs(".\\data")
            print u"创建目录 ./data"

        print u"正在爬取数据..."
        count = 0
        checked = 0
        index = self.begin
        while count < self.num:
            web_index = "1000" + self.get_web_index(index)
            path = "./data/" + web_index + '.json'
            page_data = self.get_json(web_index)

            index += 1
            checked += 1

            if checked > self.num * 10:
                print u"未找到足够资源，程序提前终止，共爬取%d项数据" % count
                break

            if page_data:
                count += 1
                output = open(path, "w")
                output.write(page_data)
                output.close()
                if count % 20 == 0:
                    print u"(%2.0f%%)已完成数量: %d， 丢弃数量: %d" % (100.0 * count / self.num, count, checked - count)

        if count == self.num:
            print u"数据全部爬取成功，已保存在data文件夹中！"


def main():
    spider = Spider()
    spider.start()


if __name__ == "__main__":
    main()
