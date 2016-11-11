# douban-crawler
## 功能
* 抓取豆瓣 https://www.douban.com/group/beijingzufang/ 小组第一页内所有发帖者的头像，并以头像用户的id作为文件名存储
* 例如，这个帖子 https://www.douban.com/group/topic/49517104/ 的发帖者"梅子", 头像应该是https://img3.doubanio.com/icon/u84097702-2.jpg 应该存储为"梅子.jpg"

## 加分项
* 由于爬虫网络可能会阻塞，请选用多线程/多进程/异步的方式来加速抓取
* 可以考虑用docker来封装爬虫，增强易用性
* 完善的使用文档
