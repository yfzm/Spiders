# -*- coding: utf-8 -*-
import codecs

import json_load

from selenium import webdriver

# ROOT_PATH = 'data/coat/'
URL_CLOTHES = 'http://shop.mogujie.com/ajax/mgj.pc.detailinfo/v1?_ajax=1&itemId='

PAGE_HEAD = 62
PAGE_TAIL = 14

coat = ['data/coat/']
skirt = ['data/skirt/']


class Labels:

    def __init__(self, category):
        self.root_path = category[0]

        self.driver = webdriver.Chrome()
        self.json = ''
        self.count = 1
        self.clothes_id = ''

    def get_json(self, page_url):
        self.driver.get(page_url)
        dom = self.driver.page_source
        self.json = dom[PAGE_HEAD:-PAGE_TAIL]

    def parse_json(self):
        obj = json_load.json_loads_byteified(self.json)
        item_list = obj['data']['itemParams']['info']['set']

        json_data = '{'
        for item in item_list:
            key = item['key'].decode('utf-8')
            value = item['value'].decode('utf-8')
            json_data += ('\"' + key + '\":\"' + value + '\",')
        json_data = json_data[:-1]
        json_data += '}'
        # print json_data

        label_file = codecs.open(self.root_path + 'label/' + self.clothes_id + '.json', 'w', 'utf-8')
        label_file.write(json_data)
        # label_file.write('{')
        # for item in item_list:
        #     key = item['key'].decode('utf-8')
        #     value = item['value'].decode('utf-8')
        #     label_file.write('\"' + key + '\":\"' + value + '\",')
        # label_file.write('}')
        label_file.close()

    def run(self):
        urls = open(self.root_path + "urls.txt", 'r')
        for url in urls:
            self.clothes_id = url.strip()
            self.get_json(URL_CLOTHES + self.clothes_id)
            self.parse_json()


if __name__ == '__main__':
    label = Labels(skirt)
    label.run()
