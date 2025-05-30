import time
import requests
import socket
import os
import logging

from config import CLIENT_CONFIG


# 获取公网 IP（使用 ipify 服务）
def get_public_ip():
    resp = requests.get('http://ip.3322.net', timeout=CLIENT_CONFIG['TIMEOUT'])
    resp.raise_for_status()
    # '36.251.0.202\n'
    text = resp.text
    ip = text.strip()
    return ip

# 通知到对端服务器
def notify_ip(ip: str):
    payload = {
        'ip': ip,
        'server_name': CLIENT_CONFIG['SERVER_NAME'] or socket.gethostname()
    }
    headers = {
        'X-API-Key': CLIENT_CONFIG['API_KEY']
    }
    try:
        r = requests.post(CLIENT_CONFIG['UPDATE_URL'], json=payload, headers=headers, timeout=CLIENT_CONFIG['TIMEOUT'])
        r.raise_for_status()
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 通知成功：服务器 {payload["server_name"]} 的IP为 {ip}')
    except Exception as e:
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 通知失败：{e}')

def main():
    # 初始化日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 检查API密钥是否已配置
    if not CLIENT_CONFIG['API_KEY']:
        print("错误：请先设置环境变量 IP_NOTIFIER_API_KEY")
        print("您可以从服务器启动时的控制台输出中获取API密钥")
        return

    last_ip = None
    server_name = CLIENT_CONFIG['SERVER_NAME'] or socket.gethostname()
    logging.info(f'CLIENT_CONFIG: {CLIENT_CONFIG}, socket.gethostname(): {server_name}')
    print(f'开始监控服务器 {server_name} 的IP变化...')
    
    while True:
        try:
            ip = get_public_ip()
        except Exception as e:
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 获取 IP 失败：{e}')
            time.sleep(CLIENT_CONFIG['INTERVAL'])
            continue

        # 如果只在 IP 变化时通知，取消下面的注释：
        # if ip != last_ip:
        notify_ip(ip)
        last_ip = ip

        time.sleep(CLIENT_CONFIG['INTERVAL'])

if __name__ == '__main__':
    main()
