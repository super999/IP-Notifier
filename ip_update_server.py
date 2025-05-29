from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os
import re
from config import SERVER_CONFIG

# 初始化 Flask 应用
app = Flask(__name__)

# 配置 logging：追加写入，并打印时间戳
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(SERVER_CONFIG['LOG_FILE'], encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 内存中保存最新 IP 和服务器信息
latest_data = {
    'ip': None,
    'server_name': None,
    'timestamp': None
}

def is_valid_ip(ip):
    """验证IP地址格式是否正确"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    # 检查每个数字是否在0-255范围内
    numbers = ip.split('.')
    return all(0 <= int(n) <= 255 for n in numbers)

@app.route('/api/update_ip', methods=['POST'])
def update_ip():
    global latest_data
    
    # 验证API密钥
    auth_header = request.headers.get('X-API-Key')
    if not auth_header or auth_header != SERVER_CONFIG['API_KEY']:
        logging.warning('未授权的访问尝试')
        return jsonify({'error': '未授权的访问'}), 401

    data = request.get_json()
    if not data or 'ip' not in data or 'server_name' not in data:
        return jsonify({'error': '请求 JSON 中缺少必要字段 (ip 或 server_name)'}), 400

    ip = data['ip']
    server_name = data['server_name']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 验证IP地址格式
    if not is_valid_ip(ip):
        logging.warning(f'收到无效的IP地址格式: {ip}')
        return jsonify({'error': '无效的IP地址格式'}), 400

    # 记录到日志
    logging.info(f'接收到 IP 更新：服务器 {server_name} 的IP为 {ip}')

    # 更新内存中的数据
    latest_data = {
        'ip': ip,
        'server_name': server_name,
        'timestamp': timestamp
    }

    # 写入文件
    with open('latest_ip.txt', 'w') as f:
        f.write(f'{server_name},{ip},{timestamp}')

    # 返回给客户端
    return jsonify({
        'status': 'success',
        'ip': ip,
        'server_name': server_name,
        'time': timestamp
    }), 200

@app.route('/api/latest_ip', methods=['GET'])
def get_latest_ip():
    """提供一个查询最新 IP 的接口"""
    if latest_data['ip'] is None:
        return jsonify({'error': '尚未收到任何 IP 更新'}), 404
    return jsonify(latest_data), 200

if __name__ == '__main__':
    # 确保日志文件存在
    if not os.path.exists(SERVER_CONFIG['LOG_FILE']):
        open(SERVER_CONFIG['LOG_FILE'], 'a').close()

    # 打印API密钥（仅用于开发环境）
    print(f'API密钥: {SERVER_CONFIG["API_KEY"]}')
    
    # 启动服务，生产环境可换成 gunicorn/Uvicorn 等
    app.run(host='0.0.0.0', port=SERVER_CONFIG['PORT'])
