
import json
import threading

import urllib.request
from queue import Queue
from random import choice

import requests
from lxml import etree

"""
使用多线程爬取数据
 1.start_url
 2.遍历所有装备名，并制成url放入列表
 3.发送请求获取响应
 4.遍历每个装备的列表，提取数据
 5.保存数据
 6.继续遍历
"""

class DarkSouls():
    user_agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",

    ]

    def __init__(self):
        self.base_item_url = "https://darksouls.wiki.fextralife.com"
        self.item_name = "/Helms"
        self.headers = {
            "User-Agent": choice(self.user_agent)}
        self.url = self.base_item_url + self.item_name
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def __repr__(self):
        return f"GetImageFile({self.item_name}, {self.base_item_url}, {self.url})"

    def mother_parse_url(self):
        response = requests.get(self.url, headers=self.headers)
        return response.content.decode()

    def get_class2_url(self, html_str):  # 获取子页面链接
        html = etree.HTML(html_str)
        div_list = html.xpath("//table[@class='wiki_table sortable']//tr//td/a[@class='wiki_link']/@href")  # 分组
        class2_url_list = []
        for div in div_list:  # 获取二级页面列表
            class2_url = self.base_item_url + div
            class2_url_list.append(class2_url)
        class2_url_list = sorted(list(set(class2_url_list)))  # 去重
        for url in class2_url_list:
            self.url_queue.put(url)

    def child_parse_url(self):  #
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            self.html_queue.put(response.content.decode())  # 将所有二级str页面放入queue中
            self.url_queue.task_done()

    def get_item_info(self):
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            div = html.xpath("//*[@id='wiki-content-block']")  # 不需要分组，提取每个整页数据
            content_list = []
            item = {}
            str = ''
            item['equipment_name'] = div[0].xpath('.//*[@id="toc0"]/text()')
            item['equipment_name'] = item['equipment_name'][0] if len(item['equipment_name']) > 0 else None
            item['description'] = div[0].xpath('.//p/em/text()')
            item['description'] = item['description'][0].replace("\"", "") if len(item['description']) > 0 else None
            item['equipment_img'] = div[0].xpath('.//table[@class="wiki_table"]//img/@src')
            item['equipment_img'] = item['equipment_img'][0] if len(item['equipment_img']) > 0 else None
            div_location = div[0].xpath(".//ul[1]/li")
            if len(div_location) > 1:
                for i in range(len(div_location)):
                    str = div_location[i].xpath("string(.)") if i == 0 else str + ',' + div_location[i].xpath(
                        "string(.)")
                item['location'] = str
            else:
                item['location'] = div_location[0].xpath("string(.)")
            div_notes = div[0].xpath(".//ul[2]/li")
            if len(div_notes) > 1:
                for i in range(len(div_notes)):
                    str = div_notes[i].xpath("string(.)") if i == 0 else str + ',' + div_notes[i].xpath("string(.)")
                item['notes'] = str
            else:
                item['notes'] = div_notes[0].xpath("string(.)")
            content_list.append(item)
            self.content_queue.put(content_list)
            self.html_queue.task_done()

    def save_data(self):  # 保存数据
        while True:
            content_list = self.content_queue.get()
            img_list = []
            path = r"image/"
            with open("Helms.txt", 'a', encoding='utf-8') as f:
                for content in content_list:
                    f.write(json.dumps(content, ensure_ascii=False, indent=2))
                    img_url = self.base_item_url + content["equipment_img"]
                    img_list.append(img_url)
                    f.write("\n")
            # 保存图片
            for content in content_list:
                with open(path + content["equipment_name"] + '.png', 'wb') as f:
                    for url in img_list:
                        url = url.replace(' ', '%20')
                        print('正在保存:', url)
                        request = urllib.request.urlopen(url)
                        buf = request.read()
                        f.write(buf)
            self.content_queue.task_done()

    def run(self):
        # 1.url_list
        thread_list = []
        html_str = self.mother_parse_url()
        t_url = threading.Thread(target=self.get_class2_url(html_str))  # 获取所有要爬取的页面的url
        thread_list.append(t_url)
        # time.sleep(random()) # 每次爬取后随机sleep以应对反爬
        # 2.遍历，发送请求，获取响应
        for i in range(20):
            t_parse = threading.Thread(target=self.child_parse_url)
            thread_list.append(t_parse)
        # 3.提取数据
        for i in range(10):
            t_html = threading.Thread(target=self.get_item_info)
            thread_list.append(t_html)
        t_save = threading.Thread(target=self.save_data)
        thread_list.append(t_save)
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，该线程不重要，主线程结束子线程结束
            t.start()
        for q in [self.url_queue, self.html_queue, self.content_queue]:
            q.join()  # 让主线程阻塞，等待队列的任务完成之后再完成


if __name__ == '__main__':
    darksouls = DarkSouls()
    darksouls.run()
