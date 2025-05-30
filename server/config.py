import secrets
import os
import json

CONFIG_FILE = 'ip_notifier_config.json'


def load_or_create_config():
    """加载或创建配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"警告：配置文件 {CONFIG_FILE} 格式错误，将创建新的配置")

    # 如果文件不存在或格式错误，创建新的配置
    config = {
        'api_key': secrets.token_hex(16),
        'server_name': os.getenv('IP_NOTIFIER_SERVER_NAME', '')
    }

    # 保存配置到文件
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"已创建新的配置文件：{CONFIG_FILE}")
        print(f"API密钥: {config['api_key']}")
    except Exception as e:
        print(f"警告：无法写入配置文件：{e}")

    return config


# 加载配置
config_data = load_or_create_config()

# 服务器配置
SERVER_CONFIG = {
    'LOG_FILE': 'ip_updates.log',  # 日志文件路径
    'PORT': 5000,  # 监听端口
    'API_KEY': os.getenv('IP_NOTIFIER_API_KEY', config_data['api_key'])  # 优先使用环境变量，否则使用配置文件中的密钥
}

# 客户端配置
CLIENT_CONFIG = {
    'UPDATE_URL': 'http://127.0.0.1:5000/api/update_ip',  # 更新服务器地址
    'INTERVAL': 1,  # 检查间隔（秒）
    'TIMEOUT': 5,  # HTTP 请求超时时间（秒）
    'API_KEY': os.getenv('IP_NOTIFIER_API_KEY', config_data['api_key']),  # 优先使用环境变量，否则使用配置文件中的密钥
    'SERVER_NAME': os.getenv('IP_NOTIFIER_SERVER_NAME', config_data['server_name'])  # 优先使用环境变量，否则使用配置文件中的名称
}