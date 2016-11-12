FROM centos 
COPY spider.py /
RUN ["yum", "install", "-y", "epel-release"]
RUN ["yum", "install", "-y", "python-pip"]
RUN ["pip", "install", "bs4"]
CMD ["nohup", "python", "spider\.py", "&"]
