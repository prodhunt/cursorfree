#!/bin/bash

# 风车cursorfree1.1l GUI版本安装脚本

set -e

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

# 获取当前目录
CURRENT_DIR=$(pwd)
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

print_info "风车cursorfree1.1l GUI版本安装程序"
print_info "当前目录: $CURRENT_DIR"
print_info "脚本目录: $SCRIPT_DIR"

# 检查Python和tkinter
print_info "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    print_error "未找到Python3，请先安装Python3"
    exit 1
fi

# 检查tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    print_warning "未找到tkinter，正在尝试安装..."
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3-tk
    elif command -v yum &> /dev/null; then
        sudo yum install -y tkinter
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-tkinter
    else
        print_error "无法自动安装tkinter，请手动安装: sudo apt install python3-tk"
        exit 1
    fi
fi

print_success "Python环境检查完成"

# 检查必要文件
print_info "检查必要文件..."
required_files=("cursor_free_gui.py" "cursor_cleaner.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$SCRIPT_DIR/$file" ]; then
        print_error "未找到必要文件: $file"
        exit 1
    fi
done

print_success "文件检查完成"

# 设置执行权限
print_info "设置执行权限..."
chmod +x "$SCRIPT_DIR/cursor_free_gui.py"
chmod +x "$SCRIPT_DIR"/*.sh

# 检查logo.ico文件
print_info "检查图标文件..."
ROOT_LOGO="$SCRIPT_DIR/../logo.ico"
LOCAL_LOGO="$SCRIPT_DIR/logo.ico"

if [ -f "$ROOT_LOGO" ]; then
    ICON_PATH="$ROOT_LOGO"
    print_success "找到根目录图标: $ROOT_LOGO"
elif [ -f "$LOCAL_LOGO" ]; then
    ICON_PATH="$LOCAL_LOGO"
    print_success "找到本地图标: $LOCAL_LOGO"
else
    # 如果没有图标文件，使用系统默认图标
    ICON_PATH="applications-development"
    print_warning "未找到logo.ico文件，使用系统默认图标"
fi

# 创建桌面文件
print_info "创建桌面文件..."
DESKTOP_FILE="$HOME/.local/share/applications/风车cursorfree1.1l.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=风车cursorfree1.1l
Name[en]=CursorFree1.1l
Comment=Cursor编辑器缓存清理工具
Comment[en]=Cursor Editor Cache Cleaner Tool
Exec=python3 "$SCRIPT_DIR/cursor_free_gui.py"
Icon=$ICON_PATH
Terminal=false
Categories=Development;Utility;
StartupNotify=true
MimeType=application/x-cursor-cleaner;
EOF

chmod +x "$DESKTOP_FILE"
print_success "桌面文件创建完成: $DESKTOP_FILE"

# 创建桌面快捷方式（可选）
if [ -d "$HOME/Desktop" ]; then
    print_info "是否在桌面创建快捷方式？(y/N)"
    read -r create_desktop
    if [[ $create_desktop =~ ^[Yy]$ ]]; then
        DESKTOP_SHORTCUT="$HOME/Desktop/风车cursorfree1.1l.desktop"
        cp "$DESKTOP_FILE" "$DESKTOP_SHORTCUT"
        chmod +x "$DESKTOP_SHORTCUT"
        print_success "桌面快捷方式创建完成: $DESKTOP_SHORTCUT"
    fi
fi

# 创建启动脚本
print_info "创建启动脚本..."
LAUNCHER_SCRIPT="$SCRIPT_DIR/start_gui.sh"
cat > "$LAUNCHER_SCRIPT" << 'EOF'
#!/bin/bash
# 风车cursorfree1.1l 启动脚本

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR"

# 检查Python和tkinter
if ! command -v python3 &> /dev/null; then
    zenity --error --text="未找到Python3，请先安装Python3" 2>/dev/null || \
    echo "错误：未找到Python3，请先安装Python3"
    exit 1
fi

if ! python3 -c "import tkinter" 2>/dev/null; then
    zenity --error --text="未找到tkinter，请安装: sudo apt install python3-tk" 2>/dev/null || \
    echo "错误：未找到tkinter，请安装: sudo apt install python3-tk"
    exit 1
fi

# 启动GUI程序
python3 "$SCRIPT_DIR/cursor_free_gui.py"
EOF

chmod +x "$LAUNCHER_SCRIPT"
print_success "启动脚本创建完成: $LAUNCHER_SCRIPT"

# 测试GUI程序
print_info "是否现在测试GUI程序？(y/N)"
read -r test_gui
if [[ $test_gui =~ ^[Yy]$ ]]; then
    print_info "启动GUI程序..."
    python3 "$SCRIPT_DIR/cursor_free_gui.py" &
    print_success "GUI程序已启动"
fi

print_success "安装完成！"
echo
print_info "使用方法："
print_info "1. 在应用程序菜单中搜索 '风车cursorfree1.1l'"
print_info "2. 双击桌面快捷方式（如果创建了）"
print_info "3. 运行启动脚本: $LAUNCHER_SCRIPT"
print_info "4. 直接运行: python3 $SCRIPT_DIR/cursor_free_gui.py"
echo
print_info "博客地址: https://xoxome.online"
