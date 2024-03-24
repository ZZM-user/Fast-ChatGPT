FROM python:3.11.8
LABEL authors="Baidu"
#基础镜像

#设置镜像的工作目录
WORKDIR /ChatGPT

#构建的时候设置环境变量
ENV DASHSCOPE_API_KEY=your_key

#把刚刚我们创建的requirements.txt文件拷贝到镜像里
COPY requirements.txt requirements.txt

#下载requirements.txt里写好的flask和redis
RUN pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

#指定8459为对外暴露的端口
EXPOSE 8459

#把当前目录拷贝进镜像里
COPY . .

#指定这个容器启动的时候要运行的命令，执行的命令为：flask run
CMD ["python3", "main.py"]
