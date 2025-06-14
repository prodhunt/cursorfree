#!/bin/bash

# 简化版Cursor清理工具启动脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误：未找到Python，请先安装Python 3.6+${NC}"
    exit 1
fi

# 检查脚本文件
if [ ! -f "cursor_cleaner.py" ]; then
    echo -e "${RED}错误：未找到cursor_cleaner.py文件${NC}"
    exit 1
fi

# 显示菜单
show_menu() {
    clear
    echo -e "${BLUE}========================================"
    echo "Cursor编辑器缓存清理工具"
    echo "========================================${NC}"
    echo
    echo "请选择操作："
    echo "1. 完整清理（推荐）"
    echo "2. 仅清理缓存"
    echo "3. 仅重置机器码"
    echo "4. 显示Cursor信息"
    echo "0. 退出"
    echo
}

# 执行命令并显示结果
run_command() {
    local cmd="$1"
    local desc="$2"
    
    echo -e "${BLUE}正在执行: $desc${NC}"
    echo "命令: $PYTHON_CMD cursor_cleaner.py $cmd"
    echo
    
    if $PYTHON_CMD cursor_cleaner.py $cmd; then
        echo
        echo -e "${GREEN}✅ $desc 执行成功${NC}"
    else
        echo
        echo -e "${RED}❌ $desc 执行失败${NC}"
    fi
    
    echo
    echo "按回车键继续..."
    read
}

# 主循环
while true; do
    show_menu
    read -p "请输入选择 (0-4): " choice
    
    case $choice in
        0)
            echo -e "${GREEN}感谢使用！${NC}"
            exit 0
            ;;
        1)
            run_command "--full" "完整清理"
            ;;
        2)
            run_command "--cache-only" "缓存清理"
            ;;
        3)
            run_command "--machine-id-only" "机器码重置"
            ;;
        4)
            run_command "--info" "显示信息"
            ;;
        *)
            echo -e "${YELLOW}无效选择，请重试！${NC}"
            sleep 1
            ;;
    esac
done
