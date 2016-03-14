#!/usr/bin/python
#coding: utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')  # 这里指定phatomjs可执行文件的位置


def main():
    print "begin"

    url = "http://bbs.byr.cn/#!board/JobInfo"
    pageId = 1

    res = precessPage(url,pageId)

    while res == 1:

        pageId = pageId + 1
        res = precessPage(url,pageId)

    driver.quit

def precessPage(url,pageId):
    print "process page: %s?p=%s\r\n" % (url,pageId)
    res = 1
    driver.get("%s?p=%s"%(url,pageId))
    # print driver.page_source

    soup = BeautifulSoup(driver.page_source)


    table = soup.find(class_="b-content")

    trs = table.find_all('tr')

    for tr in trs:
        res = precessOneTR(tr)
    time.sleep(1)
    return res

def precessOneTR(tr):
    res = 1
    tds = tr.find_all("td")

    if tr.get('class') != None:
        # print tr.get('class')
        return 1

    if len(tds) == 7:
        title = tds[1].find("a").text
        uri = tds[1].find("a").get('href')
        url_time = tds[2].text.strip()
        author = tds[3].find("a").text
        ts = url_time.split(":")

        #this recruitment information is not published today
        if len(ts) != 3:
            res = 1
            return res

        #print "title:%s \r\nurl:http://bbs.byr.cn%s\r\ntime:%s \r\nauthor:%s\r\n\r\n" % (title, uri, url_time, author)

        hasMsg = analysisOneURL(title, uri)
        if hasMsg == 1:
            print "title:%s \r\nurl:http://bbs.byr.cn%s\r\ntime:%s \r\nauthor:%s\r\n\r\n" % (title, uri, url_time, author)
    return res

def analysisOneURL(title,uri):
    url = "http://bbs.byr.cn"
    driver.get("%s%s" % (url, uri))
    print "      analysis:%s--%s%s" % (title,url, uri)
    soup = BeautifulSoup(driver.page_source)

    ct = soup.find(class_ = "a-content")

    # pattern = re.compile(r'做真极客')
    # match = pattern.match(content.text)

    pat = '户口'.decode('utf-8')

    # print content
    searchRes = re.search(pat,unicode(ct).decode('utf-8'))
    if searchRes != None:
        return 1
    # print content
    return 0
if __name__ == "__main__":
    main()