import json

from lxml import etree
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scripts.web_init import add_product
from scripts.web_init import draw_num
import time

def web_check(web):
    try:
        web.find_element('xpath', '//*[@id="J_user"]/div/div[1]/div/p[2]/span/a[2]')
        cookies = web.get_cookies()
        web.quit()
        return 'logged', cookies
    except NoSuchElementException:
        try:
            qrcode_btn = web.find_element('xpath', '//*[@id="kbCoagent"]/ul/li[2]/a')
            qrcode_btn.click()
        except NoSuchElementException:
            print('已在二维码页面')
        web.refresh()
        try:
            qrcode_img = web.find_element('xpath', "//*[@id='tpl_for_page']/span[1]/div[1]/div[4]/div[1]/img").get_attribute('src')
            return 'not logged', web, qrcode_img
        except NoSuchElementException:
            return 'not logged', web, ''

def jd_search(key, web):
    search_input = web.find_element('id', value='key')
    search_input.clear()
    search_input.send_keys(key)
    btn = web.find_element('class name', value='button')
    btn.click()
    sleep(1)
    web.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(1)
    tree = etree.HTML(web.page_source)
    goods_li_list = (tree.xpath('//div[@id="J_goodsList"]/ul/li'))
    i = 0
    for li in goods_li_list:
        i += 1
        if i > 20:
            break
        img = li.xpath('.//div[@class="p-img"]/a/img/@src')
        if not img:
            img = li.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img')
        img = 'https:' + img[0]

        title = ''.join(li.xpath('.//div[@class="p-name p-name-type-2"]/a/em//text()'))

        price = li.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
        if draw_num(price) == '':
            continue

        deal = li.xpath('.//div[@class="p-commit"]/strong/a/text()')
        if not deal:
            deal.append('none')
        deal = deal[0].strip()

        shop_name = li.xpath('.//div[@class="p-shop"]/span/a/@title')
        if not shop_name:
            shop_name.append('none')
        shop_name = shop_name[0]

        clickUrl = 'https:' + ''.join(li.xpath('.//div[@class="p-name p-name-type-2"]/a/@href'))

        platform = '京东'
        data = {}
        data['product_name'] = title
        data['platform'] = platform
        data['deal'] = deal
        data['shop_name'] = shop_name
        data['location'] = 'none'
        data['img'] = img
        data['web'] = clickUrl
        data['price'] = price

        add_product(data=data)