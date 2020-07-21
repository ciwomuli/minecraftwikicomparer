#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re


def compare(ul1, ul2):
    li_list1 = ul1.find_all(name='li')
    li_list2 = ul2.find_all(name='li')
    ret = True
    if len(li_list1) != len(li_list2):
        return False
    for i in range(0, len(li_list1)):
        if (not li_list1[i].find(name='ul')) and (not li_list2[i].find(name='ul')):
            continue
        if (li_list1[i].find(name='ul')) and (li_list2[i].find(name='ul')):
            ret = compare(li_list1[i].find(name='ul'),
                          li_list2[i].find(name='ul'))
            if(not ret):
                return False
            continue
        return False
    return True


def compareenandcn(item):
    enret = requests.get(
        url='https://minecraft.gamepedia.com' + item)
    enret.encoding = 'utf8'
    ensoup = BeautifulSoup(enret.text, 'lxml')
    endiv = ensoup.find(name='div', attrs={'class': 'toc'})
    cnurl = ensoup.find(name='li', attrs={
                        'class': 'interlanguage-link interwiki-zh'}).find(name='a').get('href')
    cnret = requests.get(url='https:' + cnurl)
    cnret.encoding = 'utf8'
    cnsoup = BeautifulSoup(cnret.text, 'lxml')
    cndiv = cnsoup.find(name='div', attrs={'class': 'toc'})
    if (not endiv) and (not cndiv):
        return True
    if endiv and cndiv:
        enul = endiv.find(name='ul')
        cnul = cndiv.find(name='ul')
        if (not enul) and (not cnul):
            return True
        if enul and cnul:
            return compare(enul, cnul)
        return False
    return False


# print(compareenandcn('/Item'))
# print(compareenandcn('/Gameplay'))
fr = open('commonpages.txt', 'r')
fw1 = open('pagesame.txt', 'w')
fw2 = open('pagedifferent.txt', 'w')
list_items = fr.readlines()
for i in range(0, len(list_items)):
    list_items[i] = list_items[i].rstrip('\n')
    print(str(i)+':'+list_items[i])
    if compareenandcn(list_items[i]):
        fw1.write(list_items[i] + '\n')
        continue
    fw2.write(list_items[i]+'\n')
fr.close()
fw1.close()
fw2.close()
