from contextlib import suppress
from os import path, mkdir
from socket import gaierror

import requests
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError
import darksouls_constant as dsr
from bs4 import BeautifulSoup as soup


class PrepIMGFiles():

    def __init__(self, category, folder_name, tag):
        """
        :param category: 使用'darksouls_constant'中的值创建 BeautifulSoup objects.
        :param folder_name: 用于创建保存爬取图片文件夹的string.
        :param tag: 包含<img src=...>的HTML tag.
        """
        self.category = category
        self.folder_name = folder_name
        self.tag = tag

    def __repr__(self):
        return f"PrepIMGFiles({self.category},{self.folder_name},{self.tag})"

    def find_img_src(self):
        data = [soup(requests.get(value).text, 'html.parser') for value in self.category.values()]
        self.create_folder_for_content()

        for items in data:
            try:
                for _tag in items.find_all(self.tag):
                    with suppress(AttributeError, TypeError):
                        GetImageFile(self.folder_name, _tag.a.img['src']).download_content()
            except KeyError:
                for _tag in items.find_all(*self.tag):
                    with suppress(AttributeError, TypeError):
                        GetImageFile(self.folder_name, _tag.a.img['src']).download_content()


    def create_folder_for_content(self):
        """新建文件夹"""
        if path.isdir(self.folder_name) is False:
            print("新建文件夹...")
            mkdir(self.folder_name)


class GetImageFile():
    def __init__(self, folder, url_path):
        """
        :param folder: 用来存放图片的文件夹.
        :param url: 网站主页.
        :param url_path: 用于parse URL的URL path .
        """
        self.folder = folder
        self.url = dsr.dsr_page
        self.url_path = url_path
        self.file_name = self.url_path.rsplit('/', 1)[-1]

    def __repr__(self):
        return f"GetImageFile({self.folder},{self.url},{self.url_path})"

    def download_content(self):
        try:
            # 下载并写入图片.
            with open(f"{self.folder}/{self.file_name}", 'wb') as f:
                print(f"Downloading {self.file_name}...")
                print("*"*50,self.url+self.url_path)
                f.write(requests.get(self.url + self.url_path).content)
                print(f"Downloading {self.file_name} successful!")
        except(gaierror, NewConnectionError, MaxRetryError, ConnectionError):
            self.download_from_img_src()

    def download_from_img_src(self):
        """出现错误时跳过下载"""
        try:
            with open(f"{self.folder}/{self.file_name}", 'wb') as f:
                print(f"Downloading {self.file_name}...")
                f.write(requests.get(self.url_path).content)
                print(f'Downloaded {self.file_name} successful!')
        except:
            pass


def main():
    equipment_categories = [
        PrepIMGFiles(dsr.spells, 'Spells', 'tr'),
        PrepIMGFiles(dsr.weapons, 'Weapons', 'tr'),
        PrepIMGFiles(dsr.shields, 'shields', ('div', {'class': 'col-sm-2'})),
        PrepIMGFiles(dsr.armor, 'Armor', 'tr'),
        PrepIMGFiles(dsr.rings, 'Rings', 'tr'),
        PrepIMGFiles(dsr.items, 'Items', 'tr')
    ]

    options_fmt = '\n|{:^50}|' * (len(equipment_categories) + 2)  # ^表示右对齐
    fmt = f"\n+{'-' * 50}+{options_fmt}\n+{'-' * 50}+\nChoose Option: "

    while True:
        user_input = input(fmt.format(
            '1. Download Spell Images ',
            '2. Download Weapon Images',
            '3. Download Shield Images',
            '4. Download Armor Images ',
            '5. Download Ring Images  ',
            '6. Download Item Images  ',
            '7. Download All Images   ',
            '8. Exit                  '
        ))

        # 按照序号下载对应图片.
        for index, equipment in enumerate(equipment_categories, 1):
            if user_input == str(index):
                equipment.find_img_src()
                break

        # 下载全部图片.
        if user_input == str(len(equipment_categories) + 1):
            for equipment in equipment_categories:
                equipment.find_img_src()


        # 退出.
        if user_input == str(len(equipment_categories) + 2):
            raise SystemExit

        # 输入错误序号时的提示.
        if user_input not in [str(num + 1) for num in range(len(equipment_categories) + 2)]:
            print(f"输入错误，请输入 1-{len(equipment_categories) + 2} 之间的数字。")


if __name__ == '__main__':
    main()
