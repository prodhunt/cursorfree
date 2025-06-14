#!/usr/bin/env python3
"""
创建简单的图标文件
"""

import tkinter as tk
from tkinter import Canvas
import os

def create_simple_icon():
    """创建一个简单的图标"""
    # 创建一个隐藏的窗口
    root = tk.Tk()
    root.withdraw()
    
    # 创建画布
    canvas = Canvas(root, width=64, height=64, bg='white')
    
    # 绘制风车图案
    # 外圆
    canvas.create_oval(10, 10, 54, 54, outline='blue', width=3, fill='lightblue')
    
    # 风车叶片
    canvas.create_polygon(32, 32, 20, 20, 32, 15, fill='red')
    canvas.create_polygon(32, 32, 44, 20, 49, 32, fill='green')
    canvas.create_polygon(32, 32, 44, 44, 32, 49, fill='yellow')
    canvas.create_polygon(32, 32, 20, 44, 15, 32, fill='orange')
    
    # 中心点
    canvas.create_oval(28, 28, 36, 36, fill='black')
    
    # 保存为PostScript文件，然后转换
    try:
        canvas.postscript(file="icon_temp.ps")
        print("图标创建完成（PostScript格式）")
    except Exception as e:
        print(f"创建图标失败: {e}")
    
    root.destroy()

def create_icon_text():
    """创建文本版本的图标信息"""
    icon_info = """
# 风车cursorfree1.1l 图标说明

由于系统限制，无法直接创建ICO格式图标。
您可以：

1. 使用现有的logo.ico文件（如果有）
2. 创建自定义图标：
   - 尺寸：64x64 或 32x32 像素
   - 格式：ICO、PNG、XPM
   - 主题：风车或清理工具相关

3. 在线图标生成器：
   - https://www.favicon-generator.org/
   - https://convertio.co/png-ico/

4. 使用系统默认图标：
   - 程序会自动使用系统默认应用图标
"""
    
    with open("icon_info.txt", "w", encoding="utf-8") as f:
        f.write(icon_info)
    
    print("图标信息已保存到 icon_info.txt")

if __name__ == "__main__":
    print("正在创建图标...")
    try:
        create_simple_icon()
    except Exception as e:
        print(f"图标创建失败: {e}")
    
    create_icon_text()
    print("完成！")
