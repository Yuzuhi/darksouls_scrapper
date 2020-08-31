# -*- coding: utf-8 -*- 
"""
用于给爬取的图片名中的乱码
"""
import os


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if ' ' in file:
                new_name = file.replace(' ', '_')
                os.rename(f'{file_dir}/{file}', new_name)
            elif '%20' in file:
                new_name = file.replace('%20', '_')
                os.rename(f'{file_dir}/{file}', new_name)
            elif '%27s' in file:
                new_name = file.replace('%27s', '_')
                os.rename(f'{file_dir}/{file}', new_name)
            elif '_-_' in file:
                new_name = file.replace('_-_', '_')
                os.rename(f'{file_dir}/{file}', new_name)

            print(file)
    # print(root)  # 当前目录路径
    # print(dirs)  # 当前路径下所有子目录
    # print(files)  # 当前路径下所有非目录子文件


for dir in ['Armor', 'Items', 'Rings', 'Shields', 'Spells', 'Weapons']:
    file_name(f'img/{dir}')
