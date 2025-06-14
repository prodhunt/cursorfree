#!/bin/bash

# 快速测试脚本

echo "=== Cursor清理工具快速测试 ==="

# 测试1: 显示信息
echo "1. 测试显示信息功能..."
python3 cursor_cleaner.py --info
echo

# 测试2: 仅重置机器码（相对安全的测试）
echo "2. 测试机器码重置功能..."
echo "注意：这将重置Cursor的机器码，请确认是否继续？(y/N)"
read -r confirm
if [[ $confirm =~ ^[Yy]$ ]]; then
    python3 cursor_cleaner.py --machine-id-only
else
    echo "跳过机器码重置测试"
fi
echo

# 测试3: 仅清理缓存
echo "3. 测试缓存清理功能..."
echo "注意：这将清理Cursor的缓存，请确认是否继续？(y/N)"
read -r confirm
if [[ $confirm =~ ^[Yy]$ ]]; then
    python3 cursor_cleaner.py --cache-only
else
    echo "跳过缓存清理测试"
fi
echo

echo "=== 测试完成 ==="
