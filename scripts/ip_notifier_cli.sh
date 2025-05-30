#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取API密钥
API_KEY=$(grep -o '"api_key": *"[^"]*"' ip_notifier_config.json | cut -d'"' -f4)
if [ -z "$API_KEY" ]; then
    echo -e "${RED}错误：无法从配置文件读取API密钥${NC}"
    exit 1
fi

# 显示菜单
show_menu() {
    clear
    echo -e "${GREEN}=== IP Notifier 管理工具 ===${NC}"
    echo "1. 查询所有服务器记录"
    echo "2. 查询特定服务器记录"
    echo "3. 查看日志"
    echo "0. 退出"
    echo -e "${YELLOW}请选择操作 [0-3]:${NC} "
}

# 查询所有服务器记录
query_all_servers() {
    echo -e "\n${GREEN}正在查询所有服务器记录...${NC}"
    curl -s http://localhost:5000/api/latest_ip | python3 -m json.tool
    echo -e "\n${YELLOW}按回车键继续...${NC}"
    read
}

# 查询特定服务器记录
query_specific_server() {
    echo -e "\n${YELLOW}请输入服务器名称:${NC} "
    read server_name
    if [ -z "$server_name" ]; then
        echo -e "${RED}错误：服务器名称不能为空${NC}"
        echo -e "\n${YELLOW}按回车键继续...${NC}"
        read
        return
    fi
    echo -e "\n${GREEN}正在查询服务器 $server_name 的记录...${NC}"
    curl -s "http://localhost:5000/api/latest_ip?server_name=$server_name" | python3 -m json.tool
    echo -e "\n${YELLOW}按回车键继续...${NC}"
    read
}

# 查看日志
view_logs() {
    echo -e "\n${GREEN}正在显示容器日志...${NC}"
    echo -e "${YELLOW}按 Ctrl+C 退出日志查看${NC}\n"
    docker-compose logs -f
}

# 主循环
while true; do
    show_menu
    read -n 1 choice
    echo

    case $choice in
        1)
            query_all_servers
            ;;
        2)
            query_specific_server
            ;;
        3)
            view_logs
            ;;
        0)
            echo -e "${GREEN}感谢使用，再见！${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}无效的选择，请重试${NC}"
            sleep 1
            ;;
    esac
done 