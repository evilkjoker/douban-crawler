#!/usr/bin/python
#-*- encoding:utf-8-*-
from bs4 import BeautifulSoup as BS 
import os 
import re 
import shutil
import threading 
import time
import urllib2

#储存路径
DIR = "./userImgs"

#下载图片全局变量,dict[filename] = imghref
testD = {}
#默认用户头像
norImgHref = "https://img3.doubanio.com/icon/user_normal.jpg"
norImg = "user_normal.jpg"

norImgPath = DIR + '/' + norImg

#topHref与 https://www.douban.com/group/beijingzufang/ 内容一致,可通过start=0 实现分页
topHref = "https://www.douban.com/group/beijingzufang/discussion?start=0"

#初始化默认用户头像
def initNorImg(nimgp):
    if not os.path.exists(nimgp):
        downAndSave(norImgHref, nimgp)

def dealUrl(url):
    headers ={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
    req = urllib2.Request(url, None, headers) 
    try:
        rsp = urllib2.urlopen(url, timeout=5)
        content = rsp.read()
    except urllib2.HTTPError, e:
    #    #raise Exception("http error " + str(e.code))
        content = ''
    return True, content

#url 正则匹配
def checkUrlS(stringl, pattern):
    return True if re.search(pattern, stringl) else False

#获取 topic 和 people 对应关系
def checkhref(alist):
    hrefl = []
    status = False
    for i in alist:
        hrefl.append(i.get('href'))
    if len(hrefl) > 1: 
        status = checkUrlS(hrefl[0], "group/topic")  
        status = checkUrlS(hrefl[1], "people")  
    else:
        pass
    return status, hrefl

#img下载
def downAndSave(img_url, filename):
    try:
        img = urllib2.urlopen(img_url)
        with open(filename, "wb") as f:
            f.write(img.read())
    except urllib2.HTTPError, e:
        print "except HTTPError" + str(e.code)

#重复时,cp&rename
def cpNorImg(nimgp, uimg):
    shutil.copy(nimgp, uimg)

#不可以通过uhref获得用户id,访问文章内容获得头像href
def mUImg(thref):
    status, html = dealUrl(thref)
    uhref = re.findall('https://img[0-9].doubanio.com/icon/u\S+?\"',html)
    if len(uhref) >= 1:
        imghref = uhref[0][:-1]
    else:
        imghref = ''
    return imghref

#可以通过uhref获得用户id,模拟头像href    
def sUImg(imghref):
    baseimgh = "https://img3.doubanio.com/icon/u" 
    postfix = imghref.split('/')[-2] + '.jpg'
    imgh = baseimgh + postfix
    return imgh

#处理a href属性      
def dealhref(sPath,hrefl):
    thref = hrefl[0]
    phref = hrefl[1]
    uidpat = '/people/[0-9]{5,12}/'
    if checkUrlS(phref, uidpat):
        imghref = sUImg(phref)
    else:     
        imghref = mUImg(thref)   
        print "check if multi " + sPath
    testD[sPath] = imghref

#入口,处理topHref
def dealIndex(href):
#n=0
    status, html = dealUrl(href)
    soup = BS(html, 'html.parser')
    for i in soup.find_all('tr'):
        alist = i.find_all('a')
        status, hrefList = checkhref(alist)
        if status:
            #回应数量
            #lastTotalN = i.find_all('td')[-2].get_text()
            #最后回复时间
            #lastReplayTime = i.find_all('td')[-1].get_text()
            #用户名
            un = alist[1].get_text()
            savePath = DIR + '/' + un.encode('utf-8') + '.jpg'   
            #check 
            if os.path.exists(savePath):
                pass
                #print "exist user img"
            else:
                dealhref(savePath, hrefList)
        else:
            pass

#total time test
def timedeco(func):
    def real_wrap(*args, **kwargs):
        a = time.time()
        res = func(*args, **kwargs)
        print "total time: " + str(time.time() - a) + " Seconds"
        return res
    return real_wrap

#程序运行,非循环
@timedeco
def run():
    if not os.path.exists(DIR): 
        os.mkdir(DIR)
    initNorImg(norImgPath)
    dealIndex(topHref)

#程序运行,循环,3min
def loop(stime=180):
    while True:
        run()
        multiTDown(testD)
        time.sleep(stime)

#由testD获得下载href和保存name
#下载头像并保存,非正常请求时使用默认头像
def newDown(nid):
    filename = testD.keys()[nid]
    imghref = testD.values()[nid]
    if imghref == norImg:
        #print "same same " + imghref 
        cpNorImg(norImgPath, filename)
    else:
        try:
            img = urllib2.urlopen(imghref, timeout=2)
            with open(filename, "wb") as f:
                f.write(img.read())
        except urllib2.HTTPError, e:
            #pass
            cpNorImg(norImgPath, filename)

def multiTDown(indict):
    startt = time.time()
    threads = []
    for i in range(len(indict.keys())):
        t = threading.Thread(target=newDown, args=(i,))
        threads.append(t)
    for i in range(len(indict.keys())):
        threads[i].start()
    for i in range(len(indict.keys())):
        threads[i].join()
    print "downloads imgs total time %s" % (time.time() - startt)

if __name__ == '__main__':
    #run()
    #multiTDown 多线程处理图片下载
    #multiTDown(testD)
    loop()