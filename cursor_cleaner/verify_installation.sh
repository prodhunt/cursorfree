#!/bin/bash

# 风车cursorfree1.1l 安装验证脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

echo -e "${BLUE}========================================"
echo "风车cursorfree1.1l 安装验证"
echo "========================================${NC}"

# 获取脚本目录
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# 1. 检查图标文件
print_info "检查图标文件..."
ROOT_LOGO="$SCRIPT_DIR/../logo.ico"
LOCAL_LOGO="$SCRIPT_DIR/logo.ico"

if [ -f "$ROOT_LOGO" ]; then
    print_success "找到根目录图标: $ROOT_LOGO"
    ICON_SIZE=$(stat -c%s "$ROOT_LOGO")
    print_info "图标文件大小: $ICON_SIZE 字节"
    file "$ROOT_LOGO"
elif [ -f "$LOCAL_LOGO" ]; then
    print_success "找到本地图标: $LOCAL_LOGO"
    ICON_SIZE=$(stat -c%s "$LOCAL_LOGO")
    print_info "图标文件大小: $ICON_SIZE 字节"
else
    print_warning "未找到图标文件"
fi

# 2. 检查桌面文件
print_info "检查桌面文件..."
DESKTOP_FILE="$HOME/.local/share/applications/风车cursorfree1.1l.desktop"
DESKTOP_SHORTCUT="$HOME/Desktop/风车cursorfree1.1l.desktop"

if [ -f "$DESKTOP_FILE" ]; then
    print_success "应用程序菜单文件存在"
    
    # 检查图标路径
    ICON_LINE=$(grep "^Icon=" "$DESKTOP_FILE")
    print_info "图标设置: $ICON_LINE"
    
    # 检查执行路径
    EXEC_LINE=$(grep "^Exec=" "$DESKTOP_FILE")
    print_info "执行路径: $EXEC_LINE"
else
    print_error "应用程序菜单文件不存在"
fi

if [ -f "$DESKTOP_SHORTCUT" ]; then
    print_success "桌面快捷方式存在"
else
    print_warning "桌面快捷方式不存在"
fi

# 3. 检查GUI程序文件
print_info "检查GUI程序文件..."
GUI_FILE="$SCRIPT_DIR/cursor_free_gui.py"

if [ -f "$GUI_FILE" ]; then
    print_success "GUI程序文件存在"
    if [ -x "$GUI_FILE" ]; then
        print_success "GUI程序文件有执行权限"
    else
        print_warning "GUI程序文件没有执行权限"
    fi
else
    print_error "GUI程序文件不存在"
fi

# 4. 检查核心功能文件
print_info "检查核心功能文件..."
CORE_FILE="$SCRIPT_DIR/cursor_cleaner.py"

if [ -f "$CORE_FILE" ]; then
    print_success "核心功能文件存在"
else
    print_error "核心功能文件不存在"
fi

# 5. 检查Python和tkinter
print_info "检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python3已安装: $PYTHON_VERSION"
    
    if python3 -c "import tkinter" 2>/dev/null; then
        print_success "tkinter可用"
    else
        print_error "tkinter不可用，请安装: sudo apt install python3-tk"
    fi
else
    print_error "Python3未安装"
fi

# 6. 测试应用程序菜单
print_info "测试应用程序菜单..."
if command -v desktop-file-validate &> /dev/null; then
    if [ -f "$DESKTOP_FILE" ]; then
        if desktop-file-validate "$DESKTOP_FILE" 2>/dev/null; then
            print_success "桌面文件格式正确"
        else
            print_warning "桌面文件格式可能有问题"
        fi
    fi
else
    print_info "desktop-file-validate未安装，跳过桌面文件验证"
fi

# 7. 显示启动方式
echo
print_info "可用的启动方式："
echo "1. 应用程序菜单: 搜索 '风车cursorfree1.1l'"
echo "2. 桌面快捷方式: 双击桌面图标"
echo "3. 启动脚本: $SCRIPT_DIR/start_gui.sh"
echo "4. 直接运行: python3 $SCRIPT_DIR/cursor_free_gui.py"

# 8. 显示博客地址
echo
print_info "博客地址: https://xoxome.online"

# 9. 询问是否测试启动
echo
print_info "是否现在测试GUI程序启动？(y/N)"
read -r test_launch
if [[ $test_launch =~ ^[Yy]$ ]]; then
    print_info "启动GUI程序..."
    python3 "$SCRIPT_DIR/cursor_free_gui.py" &
    print_success "GUI程序已在后台启动"
fi

echo
print_success "验证完成！"
