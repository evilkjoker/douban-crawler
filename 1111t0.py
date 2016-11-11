from bs4 import BeautifulSoup as BS 
import os 
import re 
import urllib2

DIR = "./userImgs/"

norImgHref = "https://img3.doubanio.com/icon/user_normal.jpg"
norImg = "user_normal.jpg"

#UA = 
#构造请求头
#try:
#    res0 = urllib2.urlopen(fphref)
#except urllib2.URLError, e:
#    print e.code

#url 正则匹配
def checkUrlS(stringl, pattern):
    return True if stringl.startswith(pattern) else False

#获取 topic 和 people 对应关系
def checkhref(alist):
    hrefl = []
    for i in alist:
        hrefl.append(i.get('href'))
    if len(hrefl) > 1:
        status = checkUrlS(hrefl[0], "group/topic")  
        status = checkUrlS(hrefl[1], "people")  
    else:
        status = False
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
#重复时,cp&rename
def cpNorImg(uimg):
    shutil.copy(norImg, uimg)

#下载头像并保存,非正常请求时使用默认头像
def downUserImg(filename, imghref):
    if imghref == norImg:
        cpNorImg(name)
    else:
        status = downAndSave(img_url, filename)
        if status:
            pass
        else:
            cpNorImg(name)


#不可以通过uhref获得用户id,访问文章内容获得头像href
def mUImg(thref):
    

#可以通过uhref获得用户id,模拟头像href    
def sUImg(imghref):
    baseimgh = "https://img3.doubanio.com/icon/u" 
    postfix = imghref.split('/')[-2] + '.jpg'
    imgh = baseimgh + postfix
    print imgh

      
def dealhref(sPath,hrefl):
    thref = hrefl[0]
    phref = hrefl[1]
    uidpat = '/people/[0-9]{5,12}/'
    if checkUrlS(phref, uidpat):
        imghref = sUImg(phref)
        print imghref
        downUserImg(sPath, imghref)  
    else:     
        #mGetUserImg(thref)    
        print "pass"

#def main():
#n=0
for i in soup.find_all('tr'):
    alist = i.find_all('a')
    status, hrefList = checkhref(alist)
    if status:
    	#回应数量
    	#lastTotalN = i.find_all('td')[-2].get_text()
    	#最后回复时间
        #lastReplayTime = i.find_all('td')[-1].get_text()
        #用户名
        unimg = alist[1].get_text() + '.jpg'
        if os.path.exists(unimg):
            pass
        else:
            savePath = DIR+'/'+unimg    
            #print savePath
            #dealhref(savePath, hrefList)
    else:
        pass

#print n #  n = 25

def run():
    if os.path.exists(DIR):
        #main()
        print "exist"
    else:
        os.mkdir(DIR)
        #main()
