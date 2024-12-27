FROM python:3.12.3-slim

WORKDIR /app

# 配置阿里云镜像源
RUN echo "deb http://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security/ bookworm-security main non-free non-free-firmware contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ bookworm-updates main non-free non-free-firmware contrib" >> /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    libssl-dev \
    libffi-dev \
    wget \
    gnupg2 \
    curl \
    unzip \
    chromium \
    chromium-driver \
    xvfb \
    dbus-x11 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置 Chrome 选项
ENV CHROME_OPTIONS="--headless --no-sandbox --disable-dev-shm-usage"
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 设置 MySQL 客户端配置环境变量
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

# 添加这些环境变量
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# 修改启动命令，添加数据初始化
CMD sh -c "python manage.py runserver 0.0.0.0:8000" 