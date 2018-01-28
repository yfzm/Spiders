# -*- coding: utf-8 -*-
import codecs

import json_load

from selenium import webdriver


class Labels:

    def __init__(self, cloth):

        self.url_clothes = 'http://shop.mogujie.com/ajax/mgj.pc.detailinfo/v1?_ajax=1&itemId='
        self.page_head = 62
        self.page_tail = 14
        config = {
            'coat': ['data/coat/'],
            'skirt': ['data/skirt/'],
            'trousers': ['data/trousers/'],
            'shoes': ['data/shoes/']
        }

        if type(cloth) != str or cloth not in config.keys():
            print 'Error: Wrong param(cloth) in Urls.__init__(self, cloth, pages)'
            return

        category = config[cloth]

        self.root_path = category[0]

        self.driver = webdriver.Chrome()
        self.json = ''
        self.count = 1
        self.clothes_id = ''

    def get_json(self, page_url):
        self.driver.get(page_url)
        dom = self.driver.page_source
        self.json = dom[self.page_head:-self.page_tail]

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

        label_file = codecs.open(self.root_path + 'label/raw/' + self.clothes_id + '.json', 'w', 'utf-8')
        label_file.write(json_data)

        label_file.close()

    def run(self):
        urls = open(self.root_path + "urls.txt", 'r')
        for url in urls:
            self.clothes_id = url.strip()
            self.get_json(self.url_clothes + self.clothes_id)
            self.parse_json()


if __name__ == '__main__':
    label = Labels('trousers')
    label.run()
