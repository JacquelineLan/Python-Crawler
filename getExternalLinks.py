# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re


#获取页面所有内链的列表
def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    #找出所有以“/”或同一网站域名开头的链接
    for link in bsObj.findAll("a",href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

#获取页面所有外链的列表
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    #找出所有以“http”或“www”开头且不包含当前url的链接
    for link in bsObj.findAll("a",href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("https://", "").split("/")
    return addressParts

#收集网站上所有外链
allExternalLinks = set()
allInternalLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    internalLinks = getInternalLinks(bsObj,splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj,splitAddress(siteUrl)[0])
    for link in externalLinks:
        if link not in allExternalLinks:
            allExternalLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in internalLinks:
            print("即将获取的链接是："+link)
            allInternalLinks.add(link)
            getAllExternalLinks(link)

getAllExternalLinks("https://baike.baidu.com")

#参考《Web Scraping with Python》一书中代码