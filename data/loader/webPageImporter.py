import re
import requests  # to install
from bs4 import BeautifulSoup  # to install
import os
from selenium import webdriver
from GUI import *


class webPageImporter:
    def __init__(self, in_site, in_gui):
        self.gui = in_gui
        self.site = str(in_site)
        self.directory = os.path.dirname(os.path.realpath(__file__)) + '/webImport/'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    # read website
    def read_website(self):
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        driver.get(self.site)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        img_tags = soup.find_all('img')
        urls = [img['src'] for img in img_tags]

        for url in urls:
            print(url)
            filename = re.search(r'/([\w_-]+[.](jpg|png))$', url)

            with open(os.path.join(self.directory, filename.group(1)), 'wb') as f:
                if 'http' not in url:
                    url = '{}{}'.format(self.site, url)
                response = requests.get(url)
                f.write(response.content)

        self.gui.update_web_page_files()
