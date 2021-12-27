# python环境
FROM python:3.8

# 暴露端口
ENV PORT 80

# 设置工作目录
WORKDIR /app/rasaweb

# 设置国内pip镜像源
COPY pip.conf /root/.pip/pip.conf

# 将当前目录文件拷贝到容器工作目录
ADD . .

RUN python -m pip install --upgrade pip==21.3.1
# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE ${PORT}

# set the user to run, don't run as root
USER 1001

# 启动wx服务
CMD ["python", "main.py", "80"]