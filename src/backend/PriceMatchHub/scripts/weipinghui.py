from lxml import etree
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from scripts.web_init import add_product
from scripts.web_init import draw_num

def web_check(web):
    try:
        web.find_element('xpath', '//*[@id="J-search"]/div[1]/a')
        cookies = web.get_cookies()
        web.quit()
        return 'logged', cookies
    except NoSuchElementException:
        try:
            qrcode_url = web.find_element('xpath', '/html/body/div[2]/div/div[1]/div[2]/div/div[1]/div/a').get_attribute('href')
            web.get(qrcode_url)
        except NoSuchElementException:
            print('...')
        web.refresh()
        try:
            qrcode_img = web.find_element('xpath', "//*[@id='tpl_for_page']/span[1]/div[1]/div[4]/div[1]/img").get_attribute('src')
            return 'not logged', web, qrcode_img
        except NoSuchElementException:
            return 'not logged', web, ''
        

def vph_search(key, web):
    # search_input = web.find_element('xpath', '//*[@id="J-search"]/div[1]/input')
    # search_input.clear()
    # search_input.send_keys(key)
    # search_input.click()
    # search_input.send_keys(Keys.ENTER)
    # search_btn = web.find_element('xpath', '//*[@id="J-search"]/div[1]/a')
    # search_btn.click()
    sleep(1)
    page_height = web.execute_script("return document.body.scrollHeight")
    viewport_height = web.execute_script("return window.innerHeight")
    current_position = 0
    while current_position < page_height * 0.2:
        web.execute_script(f"window.scrollTo(0, {current_position + viewport_height});")
        current_position += viewport_height
        sleep(2)
    tree = etree.HTML(web.page_source)
    goods_li_list = (tree.xpath('//*[@id="J_searchCatList"]/div[@class="c-goods-item  J-goods-item c-goods-item--auto-width"]'))
    i = 0
    for li in goods_li_list:
        i += 1
        if i > 20:
            break
        img = li.xpath('.//a/div[1]/div[1]/img/@src')
        if not img:
            img = li.xpath('.//a/div[1]/div[1]/img/@data-original')
        img = 'https:' + img[0]

        title = ''.join(li.xpath('.//a/div[2]/div[2]//text()'))

        price = li.xpath('.//a/div[2]/div[1]/div[1]/div[2]/text()')[0]
        if draw_num(price) == '':
            continue

        deal = 'none'

        shop_name = '唯品会官方旗舰店'

        clickUrl = 'https:' + ''.join(li.xpath('.//a/@href'))

        platform = '唯品会'
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
