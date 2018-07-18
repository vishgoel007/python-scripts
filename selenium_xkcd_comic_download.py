import requests
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


os.makedirs('newcomic', exist_ok=True)
url = r'http://xkcd.com/1663/'

# open url
brow = webdriver.Chrome()
brow.get(url=url)

while not brow.current_url.endswith('#'):
    comic_ele = brow.find_element_by_id('comic')
    prev_ele = brow.find_element_by_link_text('< Prev')
    if not comic_ele:
        print("Image not found...")
    else:
        try:
            image_ele = comic_ele.find_element_by_tag_name("img")
            img_src = image_ele.get_attribute("src")
            print('current page {}..'.format(brow.current_url))
            print('Downloading image {}...'.format(img_src))
            img_res = requests.get(url=img_src)
            img_res.raise_for_status()
        except (requests.exceptions.MissingSchema, NoSuchElementException):
            print("Not an image on that page {}..\n Downloading next image".format(brow.current_url))
            prev_ele.click()
            continue

        with open(os.path.join('newcomic', os.path.basename(img_src)), 'wb') as image_file:
            for chunk in img_res.iter_content(100000):
                image_file.write(chunk)
    prev_ele.click()

print('Downloading completed...')