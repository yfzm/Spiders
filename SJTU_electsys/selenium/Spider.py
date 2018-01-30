import codecs
import time

from selenium import webdriver, common
from PIL import Image
import pytesseract
from selenium.webdriver.support.select import Select


class Spider:
    def __init__(self, username, password):
        self.login_path = 'http://electsys.sjtu.edu.cn/edu/login.aspx'
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1200, 800)

    def get_and_save_capt(self, element):
        self.driver.get_screenshot_as_file('cache/screenshot.png')

        # left = int(element.location['x'])
        # top = int(element.location['y'])
        # right = left + int(element.size['width'])
        # bottom = top + int(element.size['height'])

        # The code above which assign left, top doesn't work for me.
        # I have to use the 'magic number' to cut the picture well.
        # However, it's a common way to get correct cut pictures using the commented code above.

        left = 1080
        top = 405
        right = left + 125
        bottom = top + 47

        im = Image.open('cache/screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save('cache/captcha.png')

    @staticmethod
    def get_ocr_capt():
        text = pytesseract.image_to_string(Image.open('cache/captcha.png'))
        return text.replace(' ', '').replace('\n', '')

    def is_succeeded(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="form-input"]/div[4]/input')
            return False
        except common.exceptions.NoSuchElementException:
            return True

    def login(self):
        count = 0
        while True:
            self.driver.get(self.login_path)
            input_user = self.driver.find_element_by_id('user')
            input_pass = self.driver.find_element_by_id('pass')
            input_capt = self.driver.find_element_by_id('captcha')
            img_capt = self.driver.find_element_by_xpath('//*[@id="form-input"]/div[3]/img')
            btn_submit = self.driver.find_element_by_xpath('//*[@id="form-input"]/div[4]/input')

            self.get_and_save_capt(img_capt)
            captcha = self.get_ocr_capt()

            input_user.send_keys(str(self.username))
            input_pass.send_keys(str(self.password))
            input_capt.send_keys(captcha)
            time.sleep(1)
            btn_submit.click()

            if self.is_succeeded():
                break

            count += 1
            if count >= 5:
                raise StandardError('Failed to log in, maybe there is something wrong with your username or password.')

    def switch_to_score(self):
        self.driver.switch_to.frame('leftFrame')
        btn_score = self.driver.find_element_by_xpath(
            '//*[@id="sdtleft"]/table/tbody/tr[2]/td[1]/table/tbody/tr[31]/td[2]/a')
        btn_score.click()
        time.sleep(3)

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame('main')
        s_year = Select(self.driver.find_element_by_id('ddlXN'))
        s_year.select_by_value('2017-2018')
        s_year = Select(self.driver.find_element_by_id('ddlXQ'))
        s_year.select_by_value('1')
        btn_search = self.driver.find_element_by_id('btnSearch')
        btn_search.click()
        time.sleep(3)

    def save_score(self):
        score_file = codecs.open('score.csv', 'w', 'gb2312')
        subjects = self.driver.find_elements_by_xpath('//*[@id="dgScore"]/tbody/tr')

        for subject in subjects:
            string_temp = ''
            for td in subject.find_elements_by_tag_name('td'):
                string_temp += (td.text.strip() + ',')
            score_file.write(string_temp[:-1] + '\n')

        score_file.close()

    def run(self):
        try:
            self.login()
            self.switch_to_score()
            self.save_score()
            print 'Succeed!'
        except StandardError as e:
            print e


if __name__ == '__main__':
    spider = Spider(username='ZhangZhe', password='glgjssyqyhfbqz')
    spider.run()
