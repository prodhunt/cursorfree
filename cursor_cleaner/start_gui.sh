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
