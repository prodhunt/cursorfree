#!/usr/bin/env python3
"""
Cursor清理工具使用示例
演示如何在代码中使用CursorCleaner类
"""

from cursor_cleaner import CursorCleaner
import time


def example_full_clean():
    """示例：完整清理"""
    print("=== 完整清理示例 ===")
    cleaner = CursorCleaner()
    
    # 显示Cursor信息
    cleaner.show_cursor_info()
    print()
    
    # 执行完整清理
    success = cleaner.full_clean()
    
    if success:
        print("✅ 完整清理成功！")
    else:
        print("❌ 完整清理失败！")


def example_cache_only():
    """示例：仅清理缓存"""
    print("=== 缓存清理示例 ===")
    cleaner = CursorCleaner()
    
    success = cleaner.cache_only_clean()
    
    if success:
        print("✅ 缓存清理成功！")
    else:
        print("❌ 缓存清理失败！")


def example_machine_id_only():
    """示例：仅重置机器码"""
    print("=== 机器码重置示例 ===")
    cleaner = CursorCleaner()
    
    success = cleaner.machine_id_only_reset()
    
    if success:
        print("✅ 机器码重置成功！")
    else:
        print("❌ 机器码重置失败！")


def example_step_by_step():
    """示例：分步执行清理"""
    print("=== 分步清理示例 ===")
    cleaner = CursorCleaner()
    
    try:
        # 获取路径信息
        paths = cleaner.get_cursor_paths()
        
        # 检查Cursor是否运行
        if cleaner.is_cursor_running():
            print("Cursor正在运行，尝试停止...")
            cleaner.stop_cursor()
            time.sleep(2)  # 等待进程完全停止
        
        # 分步执行清理
        print("1. 更新机器码...")
        cleaner.update_storage_json(paths['storage_json'])
        
        print("2. 清理状态数据库...")
        cleaner.clean_state_db(paths['state_db'])
        
        print("3. 清理缓存目录...")
        cleaner.clean_cache_directory(paths['cache'])
        
        print("4. 清理工作区存储...")
        cleaner.clean_workspace_storage(paths['workspace_storage'])
        
        print("5. 清理日志...")
        cleaner.clean_logs(paths['logs'])
        
        print("✅ 分步清理完成！")
        
    except Exception as e:
        print(f"❌ 分步清理失败: {e}")


def interactive_menu():
    """交互式菜单"""
    cleaner = CursorCleaner()
    
    while True:
        print("\n" + "="*50)
        print("Cursor编辑器缓存清理工具")
        print("="*50)
        print("1. 显示Cursor信息")
        print("2. 完整清理（推荐）")
        print("3. 仅清理缓存")
        print("4. 仅重置机器码")
        print("5. 分步清理")
        print("0. 退出")
        print("="*50)
        
        choice = input("请选择操作 (0-5): ").strip()
        
        if choice == "0":
            print("再见！")
            break
        elif choice == "1":
            cleaner.show_cursor_info()
        elif choice == "2":
            example_full_clean()
        elif choice == "3":
            example_cache_only()
        elif choice == "4":
            example_machine_id_only()
        elif choice == "5":
            example_step_by_step()
        else:
            print("无效选择，请重试！")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    # 运行交互式菜单
    interactive_menu()
