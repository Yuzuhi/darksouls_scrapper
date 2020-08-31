import requests
from lxml import etree
from bs4 import BeautifulSoup as soup

"""通过BeautifulSoup爬取rings页面数据"""


xpath_name = "//*[@id='wiki-content-block']/div/table/tbody/tr/td[@style='width: 186px; text-align: center;']/a/@href"
xpath_src = "//*[@id='wiki-content-block']//a/img"
url = 'https://darksouls.wiki.fextralife.com/rings'

header = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"}

response = requests.get(url=url, headers=header)

html = etree.HTML(response.content.decode())


div_src_list = soup(requests.get(url).text,'lxml')
div_name_list = html.xpath(xpath_name)
rings_name = [div.split('/')[1].replace('+','_') for div in div_name_list]
for index,div in enumerate(div_src_list.find_all('tr')):
    print(index,div)
    print(type(div))
    try:
        with open(f'img/Rings/{rings_name[index]}.png', 'wb') as f:
            print(url.split('rings')[0] + div.a.img['src'])
            f.write(requests.get(url.split('rings')[0]+div.a.img['src']).content)
    except:
        pass

