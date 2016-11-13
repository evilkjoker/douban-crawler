# douban-crawler
## 功能
* 抓取豆瓣 https://www.douban.com/group/beijingzufang/ 小组第一页内所有发帖者的头像，并以头像用户的id作为文件名存储
* 例如，这个帖子 https://www.douban.com/group/topic/49517104/ 的发帖者"梅子", 头像应该是https://img3.doubanio.com/icon/u84097702-2.jpg 应该存储为"梅子.jpg"

## 加分项
* 由于爬虫网络可能会阻塞，请选用多线程/多进程/异步的方式来加速抓取
* 可以考虑用docker来封装爬虫，增强易用性
* 完善的使用文档        

## 使用说明
<strong>Desc:</strong>&emsp;爬取发帖用户头像,保存在./userImgs文件夹下,无头像时为系统默认        
<strong>Require:</strong>&emsp;<code>bs4</code>       
<strong>直接运行</strong>            

* 默认循环执行,间隔时间为180秒,可通过<code>delayTime&emsp;&emsp;looprun</code>调节
* 安装bs4库,即可通过<code>python spider.py</code>开启爬虫           
 
<strong>Docker封装</strong>
           
* Docker服务开启情况下,通过<code>bash ./start.sh</code>构建名为dbcraw的镜像,并启动名为db0的容器      
  
      

