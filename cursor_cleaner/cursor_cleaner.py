#!/usr/bin/env python3
"""
Cursor编辑器缓存清理工具
支持Windows、macOS和Linux系统
自动清理缓存、重置机器码和遥测ID
"""

import os
import sys
import json
import uuid
import shutil
import platform
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class CursorCleaner:
    """Cursor编辑器缓存清理器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.home_dir = Path.home()
        self.backup_dir = Path("cursor_backup") / datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log(self, message: str, level: str = "INFO"):
        """输出日志信息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def get_cursor_paths(self) -> Dict[str, Path]:
        """获取Cursor相关路径"""
        paths = {}
        
        if self.system == "windows":
            appdata = os.environ.get('APPDATA')
            localappdata = os.environ.get('LOCALAPPDATA')
            if not appdata or not localappdata:
                raise Exception('APPDATA or LOCALAPPDATA environment variable not found')
            
            paths['user_data'] = Path(appdata) / "Cursor" / "User"
            paths['cache'] = Path(localappdata) / "cursor"
            
        elif self.system == "darwin":  # macOS
            paths['user_data'] = self.home_dir / "Library" / "Application Support" / "Cursor" / "User"
            paths['cache'] = self.home_dir / "Library" / "Caches" / "cursor"
            
        elif self.system == "linux":
            paths['user_data'] = self.home_dir / ".config" / "Cursor" / "User"
            paths['cache'] = self.home_dir / ".cache" / "cursor"
            
        else:
            raise Exception(f'Unsupported operating system: {self.system}')
        
        # 添加具体文件路径
        paths['storage_json'] = paths['user_data'] / "globalStorage" / "storage.json"
        paths['state_db'] = paths['user_data'] / "globalStorage" / "state.vscdb"
        paths['workspace_storage'] = paths['user_data'] / "workspaceStorage"
        paths['extensions'] = paths['user_data'] / "extensions"
        paths['logs'] = paths['user_data'].parent / "logs"
        
        return paths
        
    def is_cursor_running(self) -> bool:
        """检查Cursor是否正在运行"""
        try:
            if self.system == "windows":
                result = subprocess.run(['tasklist'], capture_output=True, text=True)
                return 'cursor.exe' in result.stdout.lower()
            else:
                # 更精确地查找Cursor进程，避免匹配到我们自己的脚本
                result = subprocess.run(['pgrep', '-x', 'cursor'], capture_output=True)
                if result.returncode == 0:
                    return True
                # 也检查可能的其他Cursor进程名
                result = subprocess.run(['pgrep', '-f', '/.*[Cc]ursor.*'], capture_output=True)
                return result.returncode == 0
        except Exception:
            return False

    def stop_cursor(self) -> bool:
        """尝试停止Cursor进程"""
        if not self.is_cursor_running():
            self.log("Cursor未运行")
            return True

        self.log("正在停止Cursor进程...")
        try:
            if self.system == "windows":
                subprocess.run(['taskkill', '/f', '/im', 'cursor.exe'], check=True)
            else:
                # 更安全的进程停止方式，避免杀死我们自己的脚本
                # 首先尝试精确匹配
                try:
                    subprocess.run(['pkill', '-x', 'cursor'], check=True)
                except subprocess.CalledProcessError:
                    # 如果精确匹配失败，尝试更具体的模式
                    subprocess.run(['pkill', '-f', '/.*[Cc]ursor.*'], check=True)

            self.log("Cursor进程已停止")
            return True
        except subprocess.CalledProcessError:
            self.log("无法停止Cursor进程，请手动关闭", "WARNING")
            return False
            
    def backup_file(self, file_path: Path) -> Optional[Path]:
        """备份文件"""
        if not file_path.exists():
            return None
            
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = self.backup_dir / file_path.name
        
        try:
            shutil.copy2(file_path, backup_path)
            self.log(f"已备份: {file_path} -> {backup_path}")
            return backup_path
        except Exception as e:
            self.log(f"备份失败 {file_path}: {e}", "ERROR")
            return None
            
    def generate_machine_id(self) -> str:
        """生成新的机器ID"""
        return uuid.uuid4().hex + uuid.uuid4().hex
        
    def generate_device_id(self) -> str:
        """生成新的设备ID"""
        return str(uuid.uuid4())
        
    def update_storage_json(self, storage_path: Path) -> bool:
        """更新storage.json文件中的机器码"""
        if not storage_path.exists():
            self.log(f"storage.json文件不存在: {storage_path}")
            return False
            
        # 备份原文件
        self.backup_file(storage_path)
        
        try:
            # 读取现有内容
            with open(storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 生成新的ID
            new_machine_id = self.generate_machine_id()
            new_device_id = self.generate_device_id()
            
            # 更新数据
            data['telemetry.machineId'] = new_machine_id
            data['telemetry.devDeviceId'] = new_device_id
            
            # 写回文件
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            self.log(f"已更新机器码:")
            self.log(f"  新的machineId: {new_machine_id}")
            self.log(f"  新的devDeviceId: {new_device_id}")
            return True
            
        except Exception as e:
            self.log(f"更新storage.json失败: {e}", "ERROR")
            return False
            
    def clean_cache_directory(self, cache_path: Path) -> bool:
        """清理缓存目录"""
        if not cache_path.exists():
            self.log(f"缓存目录不存在: {cache_path}")
            return True
            
        try:
            shutil.rmtree(cache_path)
            self.log(f"已清理缓存目录: {cache_path}")
            return True
        except Exception as e:
            self.log(f"清理缓存目录失败: {e}", "ERROR")
            return False
            
    def clean_state_db(self, state_db_path: Path) -> bool:
        """清理状态数据库"""
        if not state_db_path.exists():
            self.log(f"状态数据库不存在: {state_db_path}")
            return True
            
        # 备份原文件
        self.backup_file(state_db_path)
        
        try:
            state_db_path.unlink()
            self.log(f"已清理状态数据库: {state_db_path}")
            return True
        except Exception as e:
            self.log(f"清理状态数据库失败: {e}", "ERROR")
            return False
            
    def clean_workspace_storage(self, workspace_path: Path) -> bool:
        """清理工作区存储"""
        if not workspace_path.exists():
            self.log(f"工作区存储目录不存在: {workspace_path}")
            return True
            
        try:
            shutil.rmtree(workspace_path)
            self.log(f"已清理工作区存储: {workspace_path}")
            return True
        except Exception as e:
            self.log(f"清理工作区存储失败: {e}", "ERROR")
            return False
            
    def clean_logs(self, logs_path: Path) -> bool:
        """清理日志文件"""
        if not logs_path.exists():
            self.log(f"日志目录不存在: {logs_path}")
            return True

        try:
            shutil.rmtree(logs_path)
            self.log(f"已清理日志目录: {logs_path}")
            return True
        except Exception as e:
            self.log(f"清理日志目录失败: {e}", "ERROR")
            return False

    def full_clean(self) -> bool:
        """执行完整清理"""
        self.log("开始执行完整清理...")

        # 检查Cursor是否运行，如果运行则警告用户
        if self.is_cursor_running():
            self.log("⚠️  检测到Cursor正在运行", "WARNING")
            self.log("为了确保清理效果，强烈建议先关闭Cursor编辑器", "WARNING")
            self.log("继续执行清理操作...")

        try:
            paths = self.get_cursor_paths()
            success = True

            # 更新机器码
            self.log("正在更新机器码...")
            if not self.update_storage_json(paths['storage_json']):
                success = False

            # 清理状态数据库
            self.log("正在清理状态数据库...")
            if not self.clean_state_db(paths['state_db']):
                success = False

            # 清理缓存目录
            self.log("正在清理缓存目录...")
            if not self.clean_cache_directory(paths['cache']):
                success = False

            # 清理工作区存储
            self.log("正在清理工作区存储...")
            if not self.clean_workspace_storage(paths['workspace_storage']):
                success = False

            # 清理日志
            self.log("正在清理日志...")
            if not self.clean_logs(paths['logs']):
                success = False

            if success:
                self.log("✅ 完整清理成功完成！")
                self.log(f"备份文件保存在: {self.backup_dir}")
                if self.is_cursor_running():
                    self.log("⚠️  Cursor仍在运行，请重启Cursor以使更改生效", "WARNING")
                else:
                    self.log("建议重启Cursor以使更改生效")
            else:
                self.log("❌ 清理过程中出现错误，请检查日志", "WARNING")

            return success

        except Exception as e:
            self.log(f"完整清理失败: {e}", "ERROR")
            return False

    def cache_only_clean(self) -> bool:
        """仅清理缓存"""
        self.log("开始清理缓存...")

        try:
            paths = self.get_cursor_paths()
            success = self.clean_cache_directory(paths['cache'])

            if success:
                self.log("✅ 缓存清理完成！")
            else:
                self.log("❌ 缓存清理失败", "ERROR")

            return success

        except Exception as e:
            self.log(f"缓存清理失败: {e}", "ERROR")
            return False

    def machine_id_only_reset(self) -> bool:
        """仅重置机器码"""
        self.log("开始重置机器码...")

        # 检查Cursor是否运行，如果运行则警告用户
        if self.is_cursor_running():
            self.log("⚠️  检测到Cursor正在运行", "WARNING")
            self.log("为了确保修改生效，建议先关闭Cursor编辑器", "WARNING")
            self.log("继续执行重置操作...")

        try:
            paths = self.get_cursor_paths()
            success = self.update_storage_json(paths['storage_json'])

            if success:
                self.log("✅ 机器码重置完成！")
                self.log(f"备份文件保存在: {self.backup_dir}")
                if self.is_cursor_running():
                    self.log("⚠️  Cursor仍在运行，请重启Cursor以使更改生效", "WARNING")
                else:
                    self.log("建议重启Cursor以使更改生效")
            else:
                self.log("❌ 机器码重置失败", "ERROR")

            return success

        except Exception as e:
            self.log(f"机器码重置失败: {e}", "ERROR")
            return False

    def show_cursor_info(self):
        """显示Cursor相关信息"""
        self.log("Cursor编辑器信息:")
        self.log(f"操作系统: {platform.system()} {platform.release()}")
        self.log(f"Cursor运行状态: {'运行中' if self.is_cursor_running() else '未运行'}")

        try:
            paths = self.get_cursor_paths()
            self.log("Cursor路径信息:")
            for name, path in paths.items():
                exists = "✅" if path.exists() else "❌"
                self.log(f"  {name}: {exists} {path}")

        except Exception as e:
            self.log(f"获取路径信息失败: {e}", "ERROR")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Cursor编辑器缓存清理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python cursor_cleaner.py --full          # 完整清理（推荐）
  python cursor_cleaner.py --cache-only    # 仅清理缓存
  python cursor_cleaner.py --machine-id-only # 仅重置机器码
  python cursor_cleaner.py --info          # 显示Cursor信息
        """
    )

    parser.add_argument('--full', action='store_true',
                       help='执行完整清理（缓存+机器码+状态数据库）')
    parser.add_argument('--cache-only', action='store_true',
                       help='仅清理缓存目录')
    parser.add_argument('--machine-id-only', action='store_true',
                       help='仅重置机器码和遥测ID')
    parser.add_argument('--info', action='store_true',
                       help='显示Cursor相关信息')

    args = parser.parse_args()

    # 如果没有指定参数，默认执行完整清理
    if not any([args.full, args.cache_only, args.machine_id_only, args.info]):
        args.full = True

    cleaner = CursorCleaner()

    try:
        if args.info:
            cleaner.show_cursor_info()
        elif args.cache_only:
            cleaner.cache_only_clean()
        elif args.machine_id_only:
            cleaner.machine_id_only_reset()
        elif args.full:
            cleaner.full_clean()

    except KeyboardInterrupt:
        cleaner.log("操作被用户中断", "WARNING")
        sys.exit(1)
    except Exception as e:
        cleaner.log(f"程序执行出错: {e}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
