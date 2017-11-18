#六度空间问题
#通过一些词条链接寻找两个词条之间的联系
#设计一个带有两张数据表的数据库来分别存储页面和链接
#CREATE DATABASE wikipedia;
#CREATE TABLE pages (id INT NOT NULL AUTO_INCREMENT, 
#                    url VARCHAR(255) NOT NULL, 
#                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
#                    PRIMARY KEY(id))
#CREATE TABLE links (id INT NOT NULL AUTO_INCREMENT, 
#                    fromPageId INT NULL, 
#                    toPageId INT NULL, 
#                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
#                    PRIMARY KEY(id))

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='password', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")
#向pages表中插入记录
def insertPageIfNotExists(url):
    cur.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO pages (url) VALUES (%s)", (url))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]
#向links表中插入记录
def insertLink(fromPageId, toPageId):
    cur.execute("SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s", (int(fromPageId), int(toPageId)))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)", (int(fromPageId), int(toPageId)))
        conn.commit()


pages = set()
def getLinks(pageUrl, recursionLevel):
    global pages
    if recursionLevel > 4:
        return
    pageId = insertPageIfNotExists(pageUrl)
    html = urlopen("https://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        insertLink(pageId,insertPageIfNotExists(link.attrs['href']))
        if link.attrs['href'] not in pages:
            newPage = link.attrs['href']
            pages.add(newPage)
            getLinks(newPage,recursionLevel+1)

getLinks("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()