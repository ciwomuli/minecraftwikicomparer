#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re


def getnextpagenamecn(text):
    pattern = re.compile('下一页（(.*)）')
    res_list = pattern.findall(text)
    if len(res_list) == 0:
        return None
    if len(res_list) == 1:
        return res_list[0]
    print('err list length is greater than 1')
    return None


def getpagefromcn(from_name, filename):
    with open(filename, 'a', encoding='utf-8') as file_object:
        params = {'from': from_name, 'hideredirects': 1}
        ret = requests.get(
            url='https://minecraft-zh.gamepedia.com/index.php?title=Special:%E6%89%80%E6%9C%89%E9%A1%B5%E9%9D%A2', params=params)
        ret.encoding = 'utf8'
        soup = BeautifulSoup(ret.text, 'lxml')
        navdiv = soup.find(name='div', attrs={'class': 'mw-allpages-nav'})
        div = soup.find(name='div', attrs={"class": "mw-allpages-body"})
        li_list = div.find_all(name='li')
        for li in li_list:
            if not li:
                print('err li is empty')
                continue
            file_object.write(li.find(name='a').get('href') + '\n')
    return getnextpagenamecn(navdiv.text)

def getnextpagenameen(text):
    pattern = re.compile(r'Next page \((.*)\)')
    res_list = pattern.findall(text)
    if len(res_list) == 0:
        return None
    if len(res_list) == 1:
        return res_list[0]
    print('err list length is greater than 1')
    return None


def getpagefromen(from_name, filename):
    with open(filename, 'a', encoding='utf-8') as file_object:
        params = {'from': from_name, 'hideredirects': 1}
        ret = requests.get(
            url='https://minecraft.gamepedia.com/Special:AllPages', params=params)
        ret.encoding = 'utf8'
        soup = BeautifulSoup(ret.text, 'lxml')
        navdiv = soup.find(name='div', attrs={'class': 'mw-allpages-nav'})
        div = soup.find(name='div', attrs={"class": "mw-allpages-body"})
        li_list = div.find_all(name='li')
        for li in li_list:
            if not li:
                print('err li is empty')
                continue
            file_object.write(li.find(name='a').get('href') + '\n')
    return getnextpagenameen(navdiv.text)

def getallpagescn(filename):
    now = getpagefromcn('',filename)
    while now:
        now = getpagefromcn(now,filename)
        print(now)

def getallpagesen(filename):
    now = getpagefromen('',filename)
    while now:
        now = getpagefromen(now,filename)
        print(now)
        
if __name__ == "__main__":
    getallpagescn('cnallpages.txt')
    getallpagesen('enallpages.txt')
    
