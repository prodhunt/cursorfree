#!/usr/bin/env python3
"""
验证图标设置脚本
"""

import os
from pathlib import Path


def verify_icon_setup():
    """验证图标设置"""
    print("=== 验证图标设置 ===")
    
    # 检查图标文件
    script_dir = Path(__file__).parent
    root_icon = script_dir.parent / "logo.ico"
    local_icon = script_dir / "logo.ico"
    
    print(f"脚本目录: {script_dir}")
    print(f"根目录图标: {root_icon}")
    print(f"本地图标: {local_icon}")
    
    if root_icon.exists():
        print(f"✅ 找到根目录图标: {root_icon}")
        print(f"   文件大小: {root_icon.stat().st_size} 字节")
        icon_path = root_icon
    elif local_icon.exists():
        print(f"✅ 找到本地图标: {local_icon}")
        print(f"   文件大小: {local_icon.stat().st_size} 字节")
        icon_path = local_icon
    else:
        print("❌ 未找到图标文件")
        return False
    
    # 检查桌面文件
    desktop_file = Path.home() / ".local/share/applications/风车cursorfree1.1l.desktop"
    desktop_shortcut = Path.home() / "Desktop/风车cursorfree1.1l.desktop"
    
    print(f"\n=== 检查桌面文件 ===")
    
    if desktop_file.exists():
        print(f"✅ 应用程序菜单文件存在: {desktop_file}")
        with open(desktop_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if str(icon_path) in content:
                print(f"✅ 图标路径正确设置: {icon_path}")
            else:
                print(f"❌ 图标路径设置错误")
                print(f"   期望: {icon_path}")
                # 查找实际的图标行
                for line in content.split('\n'):
                    if line.startswith('Icon='):
                        print(f"   实际: {line}")
    else:
        print(f"❌ 应用程序菜单文件不存在: {desktop_file}")
    
    if desktop_shortcut.exists():
        print(f"✅ 桌面快捷方式存在: {desktop_shortcut}")
    else:
        print(f"❌ 桌面快捷方式不存在: {desktop_shortcut}")
    
    # 测试GUI程序图标设置
    print(f"\n=== 测试GUI程序图标 ===")
    try:
        import tkinter as tk
        from pathlib import Path
        
        # 模拟GUI程序的图标设置逻辑
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 首先尝试根目录的logo.ico
        root_icon = Path(__file__).parent.parent / "logo.ico"
        local_icon = Path(__file__).parent / "logo.ico"
        
        if root_icon.exists():
            try:
                root.iconbitmap(str(root_icon))
                print(f"✅ GUI程序可以使用根目录图标: {root_icon}")
            except Exception as e:
                print(f"❌ GUI程序无法使用根目录图标: {e}")
        elif local_icon.exists():
            try:
                root.iconbitmap(str(local_icon))
                print(f"✅ GUI程序可以使用本地图标: {local_icon}")
            except Exception as e:
                print(f"❌ GUI程序无法使用本地图标: {e}")
        else:
            print("❌ GUI程序找不到图标文件")
        
        root.destroy()
        
    except ImportError:
        print("❌ 无法导入tkinter，跳过GUI图标测试")
    except Exception as e:
        print(f"❌ GUI图标测试失败: {e}")
    
    return True


def show_icon_info():
    """显示图标相关信息"""
    print(f"\n=== 图标使用说明 ===")
    print("1. 菜单图标: 使用根目录的logo.ico文件")
    print("2. 窗口图标: GUI程序窗口标题栏显示的图标")
    print("3. 桌面快捷方式: 桌面上显示的图标")
    print("4. 应用程序菜单: 系统应用程序菜单中显示的图标")
    
    print(f"\n=== 图标路径优先级 ===")
    print("1. 根目录/logo.ico (优先)")
    print("2. cursor_cleaner/logo.ico (备选)")
    print("3. 系统默认图标 (最后)")


if __name__ == "__main__":
    verify_icon_setup()
    show_icon_info()
    print(f"\n=== 验证完成 ===")
