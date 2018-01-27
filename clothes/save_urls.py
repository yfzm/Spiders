import urllib

import json_load

from selenium import webdriver

URL_COAT = 'http://list.mogujie.com/search?callback=jQuery21109552696412340775_1517052183897&_version=8193&ratio=2%3A3&ad=2&_mgjuuid=4da1bba2-bf69-4f20-bed2-86a594ab7cfa&sort=pop&ptp=1.4Hibv.0.0.sNtO9j3&userId=&showH=330&cKey=15&fcid=&width=220&action=clothing&page='
URL_SKIRT = 'http://list.mogujie.com/search?callback=jQuery2110937698501530055_1517073797920&_version=8193&ratio=2%3A3&ad=2&acm=3.mf.1_0_0.0.0.0.mf_15261_805419-idx_0-mfs_20&_mgjuuid=4da1bba2-bf69-4f20-bed2-86a594ab7cfa&sort=pop&ptp=1._mf1_1239_15261.0.0.hiSTgE0&userId=&showH=330&cKey=15&fcid=50004&width=220&action=skirt&page='

END = 20

# PAGE_HEAD = 166
# PAGE_TAIL = 22

coat = [URL_COAT, 166, 22, 'data/coat/']
skirt = [URL_SKIRT, 165, 22, 'data/skirt/']


class Urls:

    def __init__(self, category):
        self.url = category[0]
        self.page_head = category[1]
        self.page_tail = category[2]
        self.root_path = category[3]

        self.driver = webdriver.Chrome()
        self.json = ''
        self.count = 1
        self.id_set = set()

    def get_json(self, page_url):
        self.driver.get(page_url)
        dom = self.driver.page_source
        self.json = dom[self.page_head:-self.page_tail]

    def parse_json(self):
        obj = json_load.json_loads_byteified(self.json)
        item_list = obj['result']['wall']['docs']

        url_file = open(self.root_path + 'urls.txt', 'a+')
        for item in item_list:
            # url_file.write(item['link'] + '\n')
            img_id = item['tradeItemId']
            if img_id not in self.id_set:
                url_file.write(img_id + '\n')
                self.id_set.add(img_id)

            img_src = item['img']
            urllib.urlretrieve(img_src, self.root_path + 'picture/' + img_id + '.jpg')
            self.count += 1

        url_file.close()

    def run(self):
        for i in range(1, END + 1):
            self.get_json(self.url + str(i))
            self.parse_json()


if __name__ == '__main__':
    url = Urls(skirt)
    url.run()
