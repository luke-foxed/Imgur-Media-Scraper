#!/usr/bin/python3

"""
Description: Script to scrape images/videos from specified search term on imgur.com  
Author: Luke Fox
"""

import os
import sys
import selenium
import time
import urllib.request
import re
from selenium import webdriver

# automatically install chromedriver rather than use local path
from webdriver_manager.chrome import ChromeDriverManager
browser = webdriver.Chrome(ChromeDriverManager().install())

# set up variables and create folder
search_term = ' '.join(sys.argv[1:])
url = 'https://imgur.com'
os.makedirs('media', exist_ok=True)

browser.get(url)
time.sleep(1.5)  # allow time for cookie banner to appear

try:
    accept_cookies = browser.find_element_by_xpath(
        '//button[text()=" I accept "]')
    accept_cookies.click()
    print('Accepting cookies...')
except:
    print('No cookie banner appeared...')
search_box = browser.find_element_by_class_name('Searchbar-textInput')
search_box.send_keys(search_term)


def main():
    i = 0
    time.sleep(0.5)
    search_button = browser.find_element_by_class_name('Searchbar-submitInput')
    search_button.click()
    time.sleep(0.1)
    browser.get(browser.current_url)  # reload required
    posts = len(browser.find_elements_by_class_name('post'))
    item = browser.find_element_by_class_name('image-list-link')
    item.click()
    while i < posts:
        get_image(i)
        get_video(i)
        i += 1
        browser.find_element_by_class_name('btn-action').click()
        time.sleep(0.5)


def get_video(counter):
    post_container = browser.find_element_by_class_name('post-image')
    try:
        video_container = post_container.find_element_by_class_name(
            'video-container')
        video_object = video_container.find_element_by_tag_name('video')
        video_source = video_object.find_element_by_tag_name('source')
        url = video_source.get_attribute('src')
        time.sleep(0.2)
        print('Downloading video | ' + url + ' saving as ' +
              'media/%s' % search_term + str(counter) + '.mp4')
        urllib.request.urlretrieve(url, 'media/%s' %
                                   search_term + str(counter) + '.mp4')
    except:
        pass


def get_image(counter):
    post_container = browser.find_element_by_class_name('post-image')
    try:
        image_url = post_container.find_element_by_tag_name('img')
        url = image_url.get_attribute('src')
        regex = re.search(("([^.]*)$"), url)  # extract extension from url
        extension = '.' + re.sub(r"\?(.*)", '', regex.group()) # append '.' and remove question marks if they exist
        time.sleep(0.2)
        print('Downloading image | ' + url + ' - saving as media/%s' %
              search_term + str(counter) + extension)
        urllib.request.urlretrieve(url, 'media/%s' %
                                   search_term + str(counter) + extension)
    except:
        pass


if __name__ == "__main__":
    main()
    browser.close()
