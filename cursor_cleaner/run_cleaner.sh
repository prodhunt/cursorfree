#!/bin/bash

# Cursor编辑器缓存清理工具启动脚本
# 支持Linux和macOS系统

# 注意：不使用 set -e，避免正常退出时被误判为错误

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python是否安装
check_python() {
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            print_error "未找到Python，请先安装Python 3.6+"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
    
    print_info "使用Python命令: $PYTHON_CMD"
}

# 检查脚本文件
check_files() {
    if [ ! -f "cursor_cleaner.py" ]; then
        print_error "未找到cursor_cleaner.py文件"
        exit 1
    fi
    
    # 确保脚本有执行权限
    chmod +x cursor_cleaner.py
}

# 显示菜单
show_menu() {
    echo
    echo "========================================"
    echo "Cursor编辑器缓存清理工具"
    echo "========================================"
    echo
    echo "请选择操作："
    echo "1. 完整清理（推荐）"
    echo "2. 仅清理缓存"
    echo "3. 仅重置机器码"
    echo "4. 显示Cursor信息"
    echo "5. 交互式示例"
    echo "0. 退出"
    echo
}

# 主菜单循环
main_menu() {
    while true; do
        show_menu
        read -p "请输入选择 (0-5): " choice
        
        case $choice in
            0)
                print_info "感谢使用！"
                exit 0
                ;;
            1)
                echo
                print_info "执行完整清理..."
                if $PYTHON_CMD cursor_cleaner.py --full; then
                    print_success "完整清理执行完成"
                else
                    print_error "完整清理执行失败"
                fi
                ;;
            2)
                echo
                print_info "执行缓存清理..."
                if $PYTHON_CMD cursor_cleaner.py --cache-only; then
                    print_success "缓存清理执行完成"
                else
                    print_error "缓存清理执行失败"
                fi
                ;;
            3)
                echo
                print_info "执行机器码重置..."
                if $PYTHON_CMD cursor_cleaner.py --machine-id-only; then
                    print_success "机器码重置执行完成"
                else
                    print_error "机器码重置执行失败"
                fi
                ;;
            4)
                echo
                print_info "显示Cursor信息..."
                if $PYTHON_CMD cursor_cleaner.py --info; then
                    print_success "信息显示完成"
                else
                    print_error "信息显示失败"
                fi
                ;;
            5)
                echo
                print_info "启动交互式示例..."
                if [ -f "example_usage.py" ]; then
                    if $PYTHON_CMD example_usage.py; then
                        print_success "交互式示例执行完成"
                    else
                        print_warning "交互式示例执行中断"
                    fi
                else
                    print_warning "未找到example_usage.py文件"
                fi
                ;;
            *)
                print_warning "无效选择，请重试！"
                ;;
        esac
        
        echo
        read -p "按回车键继续..."
    done
}

# 主函数
main() {
    print_info "Cursor编辑器缓存清理工具启动中..."
    
    # 检查环境
    check_python
    check_files
    
    # 如果有命令行参数，直接执行
    if [ $# -gt 0 ]; then
        print_info "执行命令: $PYTHON_CMD cursor_cleaner.py $*"
        if $PYTHON_CMD cursor_cleaner.py "$@"; then
            print_success "命令执行完成"
            exit 0
        else
            print_error "命令执行失败"
            exit 1
        fi
    fi
    
    # 否则显示交互菜单
    main_menu
}

# 脚本入口
main "$@"
