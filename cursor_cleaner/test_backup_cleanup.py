#!/usr/bin/env python3
"""
测试清理备份文件功能
"""

import os
import shutil
from pathlib import Path
import tempfile
import json
from datetime import datetime


def create_test_backup():
    """创建测试备份文件"""
    print("=== 创建测试备份文件 ===")
    
    backup_dir = Path("cursor_backup")
    
    # 创建多个备份目录
    test_dirs = [
        backup_dir / "20250529_100000",
        backup_dir / "20250529_110000", 
        backup_dir / "20250529_120000"
    ]
    
    for test_dir in test_dirs:
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建测试文件
        storage_file = test_dir / "storage.json"
        test_data = {
            "telemetry.machineId": "test_machine_id_12345",
            "telemetry.devDeviceId": "test_device_id_67890",
            "test.timestamp": datetime.now().isoformat()
        }
        
        with open(storage_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2)
        
        # 创建一些额外的测试文件
        (test_dir / "test_file.txt").write_text("这是一个测试文件")
        (test_dir / "another_file.log").write_text("测试日志内容")
        
        print(f"✅ 创建测试目录: {test_dir}")
    
    return backup_dir


def get_backup_info(backup_dir):
    """获取备份目录信息"""
    if not backup_dir.exists():
        return 0, 0
    
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.exists():
                total_size += file_path.stat().st_size
                file_count += 1
    
    return file_count, total_size


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def test_backup_cleanup():
    """测试备份清理功能"""
    print("=== 测试备份清理功能 ===")
    
    # 创建测试备份
    backup_dir = create_test_backup()
    
    # 获取创建后的信息
    file_count, total_size = get_backup_info(backup_dir)
    print(f"\n📊 备份目录信息:")
    print(f"   目录: {backup_dir.absolute()}")
    print(f"   文件数量: {file_count}")
    print(f"   占用空间: {format_size(total_size)}")
    
    # 模拟清理操作
    print(f"\n🗑️ 模拟清理备份文件...")
    print(f"   即将删除: {backup_dir.absolute()}")
    print(f"   文件数量: {file_count}")
    print(f"   释放空间: {format_size(total_size)}")
    
    # 询问是否真的删除
    response = input("\n是否真的删除测试备份文件？(y/N): ")
    if response.lower() == 'y':
        try:
            shutil.rmtree(backup_dir)
            print("✅ 测试备份文件已删除")
            print("✅ 清理备份文件功能测试通过")
        except Exception as e:
            print(f"❌ 删除失败: {e}")
    else:
        print("⏭️ 跳过删除，保留测试文件")
        print("💡 您可以手动测试GUI中的'清理备份文件'按钮")


def test_gui_integration():
    """测试GUI集成"""
    print("\n=== GUI集成测试建议 ===")
    print("1. 启动GUI程序: python3 cursor_free_gui.py")
    print("2. 点击'清理备份文件'按钮")
    print("3. 查看确认对话框中的信息是否正确")
    print("4. 确认删除后检查备份目录是否被删除")
    print("5. 查看日志输出是否正常")


def main():
    """主函数"""
    print("备份文件清理功能测试")
    print("=" * 40)
    
    try:
        test_backup_cleanup()
        test_gui_integration()
        
        print("\n" + "=" * 40)
        print("✅ 测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    main()
