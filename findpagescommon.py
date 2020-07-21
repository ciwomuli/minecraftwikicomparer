import requests
from bs4 import BeautifulSoup
import re

fr = open('enallpages.txt', 'r')
fw1 = open('commonpages.txt', 'w')
fw2 = open('incommonpages.txt', 'w')

def findcninen(item,fw1,fw2):
    ret = requests.get(
        url='https://minecraft.gamepedia.com' + item)
    ret.encoding = 'utf8'
    soup = BeautifulSoup(ret.text, 'lxml')
    cnli_list = soup.find_all(name='li', attrs={'class': 'interlanguage-link interwiki-zh'})
    if len(cnli_list) == 0:
        fw2.write(item + '\n')
        return
    if len(cnli_list) == 1:
        fw1.write(item + '\n')
        return
    print('err have two or more chinese li')

list_items = fr.readlines()
for i in range(0, len(list_items)):
    list_items[i] = list_items[i].rstrip('\n')
    print(str(i) + ':' + list_items[i])
    findcninen(list_items[i],fw1,fw2)

fr.close()
fw1.close()
fw2.close()
    
