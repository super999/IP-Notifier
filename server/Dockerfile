FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建日志目录并设置权限
RUN mkdir -p /app/logs && \
    touch /app/ip_updates.log && \
    chmod 666 /app/ip_updates.log

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "ip_update_server.py"] 