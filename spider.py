#!/usr/bin/python
#-*- encoding:utf-8-*-
from bs4 import BeautifulSoup as BS 
import os 
import re 
import shutil
import time
import urllib2



DIR = "./userImgs"

norImgHref = "https://img3.doubanio.com/icon/user_normal.jpg"
norImg = "user_normal.jpg"
norImgPath = DIR + '/' + norImg

#topHref与 https://www.douban.com/group/beijingzufang/ 内容一致,可通过start=0 实现分页
topHref = "https://www.douban.com/group/beijingzufang/discussion?start=0"

def dealUrl(url):
    headers ={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
    req = urllib2.Request(url, None, headers) 
    rsp = urllib2.urlopen(req)
    return rsp.read()

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
    status = False
    try:
        img = urllib2.urlopen(img_url)
        if img.headers.maintype == 'image':
            with open(filename, "wb") as f:
                f.write(img.read())
            status = True
    except:
        pass
    return status

def initNorImg(nimgp):
    if os.path.exists(nimgp):
        pass
    else:
        downAndSave(norImgHref, nimgp)
#重复时,cp&rename
def cpNorImg(nimgp, uimg):
    shutil.copy(nimgp, uimg)

#下载头像并保存,非正常请求时使用默认头像
def downUserImg(filename, imghref):
    if imghref == norImg:
        cpNorImg(norImgPath, filename)
    else:
        status = downAndSave(imghref, filename)
        if status:
            pass
        else:
            cpNorImg(norImgPath, filename)


#不可以通过uhref获得用户id,访问文章内容获得头像href
def mUImg(thref):
    html = dealUrl(thref)
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

      
def dealhref(sPath,hrefl):
    thref = hrefl[0]
    phref = hrefl[1]
    uidpat = '/people/[0-9]{5,12}/'
    if checkUrlS(phref, uidpat):
        imghref = sUImg(phref)
        downUserImg(sPath, imghref)  
        print "simp href " + phref
    else:     
        imghref = mUImg(thref)   
        downUserImg(sPath, imghref)  
        print "check if multi " + sPath
        print phref

def main():
#n=0
    html = dealUrl(topHref)
    soup = BS(html, 'lxml')
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
            savePath = DIR + '/' + un + '.jpg'   
            print savePath
            #check 
            if os.path.exists(savePath):
                pass
                print "exist user img"
            else:
                dealhref(savePath, hrefList)
        else:
            pass
        print ''
#total time test
def timedeco(func):
    def real_wrap(*args, **kwargs):
        a = time.time()
        res = func(*args, **kwargs)
        print "total time: " + str(time.time() - a) + " Seconds"
        return res
    return real_wrap

@timedeco
def run():
    if os.path.exists(DIR):
        initNorImg(norImgPath)
        main()
        print "exist dir"
    else:
        os.mkdir(DIR)
        initNorImg(norImgPath)
        main()
#run()
#average 1page/4.8s
def loop(stime=180):
    while True:
        run()
        time.sleep(stime)
