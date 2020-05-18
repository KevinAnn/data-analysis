# coding=utf-8
import requests

from bs4 import BeautifulSoup

req = requests.get('https://www.worldometers.info/coronavirus/')
req.encoding = 'utf-8'

soup = BeautifulSoup(req.text, 'html.parser')

result = soup.find(attrs={'id': 'main_table_countries_today'}).find('tbody').find_all('tr')

for tr in result:
    if not tr.has_attr('class'):
        # 国家
        print(tr.find_all('td')[1].text)
        # 确诊人数
        print(tr.find_all('td')[2].text)


# print(result)


print(len(123))