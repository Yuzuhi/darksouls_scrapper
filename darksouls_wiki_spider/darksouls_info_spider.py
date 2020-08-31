import json
import random
from os import mkdir, path
import requests
from lxml import etree
from requests.exceptions import ProxyError
import re
import unicodedata
import darksouls_constant as dsr

# gobal productid
productid = 0

"""
 1.start_url
 2.遍历所有装备名，并制成url放入列表
 3.发送请求获取响应
 4.遍历每个装备的列表，提取数据
 5.保存数据
 6.继续遍历

-------------------
需要提取所有子装备的链接，然后放在list里，最后再遍历，爬取，保存
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

    def __init__(self, category, folder_name, xpath, equipment_name_xpath=dsr.default_equipment_name_xpath):
        self.category = category
        self.headers = {
            "User-Agent": random.choice(self.user_agent)}
        self.folder_name = folder_name
        self.xpath = xpath
        self.equipment_name_xpath = equipment_name_xpath

    def mother_parse_url_list(self, url_value):
        response = requests.get(url_value, headers=self.headers)
        return response

    def child_parse_url(self, url):  # parse最小的子页面
        try:
            return requests.get(url, headers=self.headers).content.decode()
        except ProxyError:
            url = url.split('com', 1)[1]
            return requests.get(url, headers=self.headers).content.decode()

    # 将所有子页面的武器url提取出来放入列表
    # 要提取url就需要etree解析html

    def get_class2_url(self, html_str):  # 获取子页面链接
        class2_url_child_list = []
        html = etree.HTML(html_str.content.decode())
        div_list = html.xpath(self.xpath)  # 分组
        for div in div_list:
            class2_url = dsr.dsr_page + div
            class2_url_child_list.append(class2_url)
        class2_url_child_list = sorted(list(set(class2_url_child_list)))  # 去重
        return class2_url_child_list

    def get_item_info(self, html_str, url_key):
        html = etree.HTML(html_str)
        div = html.xpath("//*[@id='wiki-content-block']")  # 不需要分组，提取每个整页数据
        content_list = []
        item = {}
        string = ''
        product = div[0].xpath(self.equipment_name_xpath)
        item['productname'] = product[0].rsplit('/', 1)[-1].rsplit('.', 1)[0] if len(product) > 0 else None
        if item['productname'] != None:
            item['productname'] = item['productname'].replace('%20', '_').replace(' ','_')
        item['productlongname'] = div[0].xpath('.//p/em/text()')
        item['productlongname'] = item['productlongname'][0].replace("\"", "") if len(
            item['productlongname']) > 0 else None
        div_location = div[0].xpath(".//ul[1]/li")
        if len(div_location) > 1:
            for i in range(len(div_location)):
                string = div_location[i].xpath("string(.)") if i == 0 else string + ',' + div_location[i].xpath(
                    "string(.)")
            item['location'] = string
        else:
            item['location'] = div_location[0].xpath("string(.)")
        div_notes = div[0].xpath("//*[contains(text(),'Notes')]/following-sibling::ul[1]")
        if div_notes is False:
            if len(div_notes) > 1:
                for i in range(len(div_notes)):
                    string = div_notes[i].xpath("string(.)") if i == 0 else string + ',' + div_notes[i].xpath(
                        "string(.)")
                item['notes'] = string
            else:
                item['notes'] = div_notes[0].xpath("string(.)")
        self.add_customize_item(item, url_key)
        content_list.append(item)
        return content_list

    def create_folder_for_content(self):
        """新建文件夹"""
        if path.isdir(self.folder_name) is False:
            print("新建文件夹...")
            mkdir(self.folder_name)

    def save_data(self, content_list):  # 保存数据
        self.create_folder_for_content()
        with open(f"img/{self.folder_name}/{self.folder_name}.txt", 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))

    def save_sql_data(self, content_list):
        """保存用于直接导入sql所需要的的数据"""
        with open(f"img/{self.folder_name}/{self.folder_name}.txt", 'a', encoding='utf-8') as f:
            for content in content_list:
                dict_valuse = unicodedata.normalize("NFKC",
                                                    re.findall("dict_values.*?\\[(.*?)\\].*?", str(content.values()))[
                                                        0])
                dict_valuse = dict_valuse.replace('None', 'null')
                f.write('insert into dark_souls_goods\n')
                f.write('(')
                for index, key in enumerate(content.keys()):
                    if index <= 10:
                        f.write(f'{key},')
                    else:
                        f.write(f'{key}')
                f.write(') values\n')
                f.write(f'({dict_valuse});\n')

    def save_main_show_data(self, content_list, main_show_dict, count):
        """保存数据库中的main_show table所需要的的数据"""
        for content in content_list:
            main_show_dict[f'productimg{count}'] = content['productimg']
            main_show_dict[f'productlongname{count}'] = content['productlongname']
            main_show_dict[f'price{count}'] = content['price']
            main_show_dict[f'marketprice{count}'] = content['marketprice']
        return main_show_dict

    def write_main_show_data(self,  main_show_dict):
        """写入数据库中的main_show table所需要的的数据"""
        with open(f"img/{self.folder_name}/save_main_show_data.txt", 'a', encoding='utf-8') as f:
                dict_valuse = unicodedata.normalize("NFKC", re.findall("dict_values.*?\\[(.*?)\\].*?",
                                                                       str(main_show_dict.values()))[0])
                dict_valuse = dict_valuse.replace('None', 'null')
                f.write('insert into yuzuhi_mainshow\n')
                f.write('(')
                for index, key in enumerate(main_show_dict.keys()):
                    if index <= 10:
                        f.write(f'{key},')
                    else:
                        f.write(f'{key}')
                f.write(') values\n')
                f.write(f'({unicodedata.normalize("NFKC", dict_valuse)});\n')

    def add_customize_item(self, item, url_key):
        """写入自定义的数据"""
        global productid #由于所有数据的productid均需要不同，因此使用全局变量
        productid += 1
        for index, category in enumerate(dsr.CATEGORY_LIST):
            productnum = random.randint(1, 5000)
            item['productid'] = productid
            if self.folder_name == category:
                item['categoryid'] = f'000{index}'
            item['specifics'] = f'{productnum} people bought this'
            item['childcidname'] = url_key
            item['childcid'] = sum([ord(char) for char in url_key])
            item['productimg'] = rf"img/{self.folder_name}/{item['productname']}.png".replace(' ', '_')
            item['productnum'] = productnum
            if index == 0:
                item['price'] = random.randint(499, 1199)
            elif index == 1:
                item['price'] = random.randint(699, 2001)
            elif index == 2:
                item['price'] = random.randint(699, 1809)
            elif index == 3:
                item['price'] = random.randint(599, 4101)
            elif index == 4:
                item['price'] = random.randint(699, 1809)
            elif index == 5:
                item['price'] = random.randint(9, 501)
        item['marketprice'] = round(item['price'] * 1.2, 2)

    def run(self):
        count = 0
        main_show_dict = {}
        for url_key, url_value in self.category.items():
            html_str = self.mother_parse_url_list(url_value)
            class2_url_mother_list = self.get_class2_url(html_str)  # 获取所有要爬取的当前分类的url
            for url in class2_url_mother_list:
                if url.find('(Upgraded)') >= 0:
                    class2_url_mother_list.remove(url)
            for url in class2_url_mother_list:  # 遍历子页面
                count += 1
                print('url', url)
                html_str = self.child_parse_url(url)
                content_list = self.get_item_info(html_str, url_key)
                print(content_list)
                self.save_sql_data(content_list)
                main_show_dict = self.save_main_show_data(content_list, main_show_dict, count)
                if count == 3:
                    self.write_main_show_data( main_show_dict)
                    count = 0


def main():
    equipment_categories = [
        DarkSouls(dsr.spells, 'Spells', dsr.xpath_spells, dsr.spells_equipment_name_xpath),
        DarkSouls(dsr.weapons, 'Weapons', dsr.xpath_weapons),
        DarkSouls(dsr.shields, 'Shields', dsr.xpath_shields),
        DarkSouls(dsr.armor, 'Armor', dsr.xpath_armor),
        DarkSouls(dsr.rings, 'Rings', dsr.xpath_rings, dsr.rings_items_equipment_name_xpath),
        DarkSouls(dsr.items, 'Items', dsr.xpath_items, dsr.rings_items_equipment_name_xpath),
    ]

    # Set format string for 'user_input' based on the number of objects in 'equipment_categories'.
    options_fmt = '\n|{:^50}|' * (len(equipment_categories) + 2)  # ^表示右对齐
    fmt = f"\n+{'-' * 50}+{options_fmt}\n+{'-' * 50}+\nChoose Option: "

    while True:
        user_input = input(fmt.format(
            '1. Download Spell Info ',
            '2. Download Weapon Info',
            '3. Download Shield Info',
            '4. Download Armor Info ',
            '5. Download Ring Info  ',
            '6. Download Item Info  ',
            '7. Download All Info   ',
            '8. Exit                '
        ))

        # 按照序号下载对应info.
        for index, equipment in enumerate(equipment_categories, 1):
            if user_input == str(index):
                equipment.run()
                break

        # 下载全部info.
        for equipment in equipment_categories:
            equipment.run()

        # 退出.
        if user_input == str(len(equipment_categories) + 2):
            raise SystemExit

        # 输入错误序号时的提示.
        if user_input not in [str(num + 1) for num in range(len(equipment_categories) + 2)]:
            print(f"输入错误，请输入 1-{len(equipment_categories) + 2} 之间的数字。")


if __name__ == '__main__':
    main()
