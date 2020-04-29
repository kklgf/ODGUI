import re
import requests  # to install
from bs4 import BeautifulSoup  # to install
import os
from selenium import webdriver

site = 'http://pixabay.com'
directory = os.path.dirname(os.path.realpath(__file__)) + '/webImport/'
if not os.path.exists(directory):
    os.makedirs(directory)

#read website
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
driver.get(site)
soup = BeautifulSoup(driver.page_source, 'html.parser')

img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]

for url in urls:
    print(url)
    filename = re.search(r'/([\w_-]+[.](jpg|png))$', url)  #  maybe look for gifs too?  

    with open(os.path.join(directory, filename.group(1)), 'wb') as f:
        if 'http' not in url:
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)
