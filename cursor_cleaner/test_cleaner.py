#!/usr/bin/env python3
"""
Cursor清理工具测试脚本
用于测试各项功能是否正常工作
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from cursor_cleaner import CursorCleaner


def test_path_detection():
    """测试路径检测功能"""
    print("=== 测试路径检测 ===")
    
    try:
        cleaner = CursorCleaner()
        paths = cleaner.get_cursor_paths()
        
        print(f"✅ 系统类型: {cleaner.system}")
        print("✅ 路径检测成功:")
        for name, path in paths.items():
            exists = "✅" if path.exists() else "❌"
            print(f"  {name}: {exists} {path}")
        
        return True
    except Exception as e:
        print(f"❌ 路径检测失败: {e}")
        return False


def test_cursor_process_detection():
    """测试Cursor进程检测"""
    print("\n=== 测试进程检测 ===")
    
    try:
        cleaner = CursorCleaner()
        is_running = cleaner.is_cursor_running()
        
        print(f"✅ Cursor运行状态: {'运行中' if is_running else '未运行'}")
        return True
    except Exception as e:
        print(f"❌ 进程检测失败: {e}")
        return False


def test_id_generation():
    """测试ID生成功能"""
    print("\n=== 测试ID生成 ===")
    
    try:
        cleaner = CursorCleaner()
        
        machine_id = cleaner.generate_machine_id()
        device_id = cleaner.generate_device_id()
        
        print(f"✅ 机器ID生成: {machine_id} (长度: {len(machine_id)})")
        print(f"✅ 设备ID生成: {device_id}")
        
        # 验证ID格式
        if len(machine_id) == 64:  # 两个UUID的hex字符串
            print("✅ 机器ID格式正确")
        else:
            print("❌ 机器ID格式错误")
            return False
            
        return True
    except Exception as e:
        print(f"❌ ID生成失败: {e}")
        return False


def test_backup_functionality():
    """测试备份功能"""
    print("\n=== 测试备份功能 ===")
    
    try:
        cleaner = CursorCleaner()
        
        # 创建临时文件进行测试
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            test_data = {"test": "data", "number": 123}
            json.dump(test_data, f)
            temp_file = Path(f.name)
        
        # 测试备份
        backup_path = cleaner.backup_file(temp_file)
        
        if backup_path and backup_path.exists():
            print(f"✅ 备份功能正常: {backup_path}")
            
            # 验证备份内容
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            if backup_data == test_data:
                print("✅ 备份内容正确")
                result = True
            else:
                print("❌ 备份内容不匹配")
                result = False
        else:
            print("❌ 备份失败")
            result = False
        
        # 清理临时文件
        temp_file.unlink(missing_ok=True)
        if backup_path:
            backup_path.unlink(missing_ok=True)
        
        return result
        
    except Exception as e:
        print(f"❌ 备份功能测试失败: {e}")
        return False


def test_storage_json_update():
    """测试storage.json更新功能"""
    print("\n=== 测试storage.json更新 ===")
    
    try:
        cleaner = CursorCleaner()
        
        # 创建临时storage.json文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            test_data = {
                "telemetry.machineId": "old_machine_id",
                "telemetry.devDeviceId": "old_device_id",
                "other.setting": "should_remain"
            }
            json.dump(test_data, f)
            temp_file = Path(f.name)
        
        # 测试更新
        success = cleaner.update_storage_json(temp_file)
        
        if success:
            # 验证更新结果
            with open(temp_file, 'r') as f:
                updated_data = json.load(f)
            
            if (updated_data['telemetry.machineId'] != "old_machine_id" and
                updated_data['telemetry.devDeviceId'] != "old_device_id" and
                updated_data['other.setting'] == "should_remain"):
                print("✅ storage.json更新功能正常")
                print(f"  新机器ID: {updated_data['telemetry.machineId']}")
                print(f"  新设备ID: {updated_data['telemetry.devDeviceId']}")
                result = True
            else:
                print("❌ storage.json更新内容错误")
                result = False
        else:
            print("❌ storage.json更新失败")
            result = False
        
        # 清理临时文件
        temp_file.unlink(missing_ok=True)
        
        return result
        
    except Exception as e:
        print(f"❌ storage.json更新测试失败: {e}")
        return False


def test_info_display():
    """测试信息显示功能"""
    print("\n=== 测试信息显示 ===")
    
    try:
        cleaner = CursorCleaner()
        cleaner.show_cursor_info()
        print("✅ 信息显示功能正常")
        return True
    except Exception as e:
        print(f"❌ 信息显示失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("Cursor清理工具功能测试")
    print("=" * 50)
    
    tests = [
        ("路径检测", test_path_detection),
        ("进程检测", test_cursor_process_detection),
        ("ID生成", test_id_generation),
        ("备份功能", test_backup_functionality),
        ("storage.json更新", test_storage_json_update),
        ("信息显示", test_info_display),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关功能")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
