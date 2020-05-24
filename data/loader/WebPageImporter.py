import re
import requests  # to install
from bs4 import BeautifulSoup  # to install
import os
from selenium import webdriver #to install
from data.GUI.GUI import *


class WebPageImporter:
    def __init__(self, gui):
        self.gui = gui
        self.site = None
        self.directory = os.path.dirname(os.path.realpath(__file__)) + '/webImport/'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        # gui.folderpath[0] = self.directory

    # read website
    def read_website(self, in_site: str) -> None:
        self.site = str(in_site)
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
                print('ok')
        #self.gui.update_web_page_files()
