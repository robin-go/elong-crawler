import requests
from lxml import etree
from selenium import webdriver
import csv
import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s : %(message)s')
logger = logging.getLogger('spider')
logger.setLevel(logging.INFO)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
url0 = 'http://hotel.elong.com/'
count = 1
detail_abandon = []
list_abandon = []


# 列表页爬取
def list_crawl(i):
    next_button = browser.find_element_by_class_name('page_next')
    next_button.click()
    browser.implicitly_wait(10)  # 隐性等待10秒（提前完成则进下一步， 10秒未完成则报错）
    html = etree.HTML(browser.page_source)
    hotel_ids = html.xpath('//div[@class="h_item mvt_171218"]//p[@class="h_info_b1"]/a/@href')
    hotel_ids = [hotel_id[1:-1] for hotel_id in hotel_ids]
    logger.info('列表页%s 爬取成功' % i)
    return hotel_ids


# 详情页爬取
def detail_crawl(hotel_id):
    global count
    response = requests.get(url=url0 + hotel_id, headers=headers, timeout=2)

    # 判断爬取是否成功
    if response.status_code == 200:
        logger.info('第%d个, %s 爬取成功 %d' % (count, hotel_id, response.status_code))
    else:
        raise Exception('%s 爬取失败 %d 程序结束 共爬取%d个' % (hotel_id, response.status_code, count))

    response = etree.HTML(response.content)
    name = response.xpath('//div[@class="t24 yahei"]/h1/text()')[0]
    address_tag = response.xpath('//span[@class="mr5 left"]/text()')
    address = [addr.strip() for addr in address_tag if addr.strip()][0]
    title = response.xpath('//div[@class="t24 yahei"]/b/@title')
    star = title[0] if title else ''
    telephone = response.xpath('//div[@class="dview_info"]/dl[1]/dd/text()')[0].strip()

    # 保存到csv文件
    info_list = [name, address, star, telephone]
    with open('hotel.csv', 'a') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(info_list)

    count += 1
    time.sleep(1)


def main():
    # 爬取首页
    browser.get('http://hotel.elong.com/wuhan/')
    html = etree.HTML(browser.page_source)
    hotel_ids = html.xpath('//div[@class="h_item mvt_171218"]//p[@class="h_info_b1"]/a/@href')
    hotel_ids = [hotel_id[1:-1] for hotel_id in hotel_ids]
    for hotel_id in hotel_ids:
        detail_crawl(hotel_id)

    # 2到283页
    for i in range(19, 285):
        try:
            hotel_ids = list_crawl(i)
            for hotel_id in hotel_ids:
                try:
                    detail_crawl(hotel_id)
                # 捕获报错的详情页并记录下来
                except Exception as e:
                    logger.error(e)
                    detail_abandon.append(hotel_id)
        # 捕获报错的列表页并记录下来
        except Exception as e:
            logger.error(e)
            list_abandon.append(i)


    with open('list_abandon.txt', 'w') as f:
        for page in list_abandon:
            f.write(page + '\n')

    with open('detail_abandon.txt', 'w') as f:
        for hotel_id in detail_abandon:
            f.write(hotel_id + '\n')

    browser.close()
    logger.info('Mission Complete. Congratulations!')


if __name__ == '__main__':
    browser = webdriver.Firefox()
    main()
