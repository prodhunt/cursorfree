# 故障排除指南

## 🐛 常见问题及解决方案

### 问题1: 运行 `./run_cleaner.sh` 出现 "Terminated" 错误

**症状**：
- 直接运行 `./run_cleaner.sh` 时脚本被终止
- 显示 "Terminated" 消息
- 但分步执行菜单功能正常

**原因分析**：
1. 原始脚本使用了 `set -e`，导致任何非零退出状态都会终止脚本
2. Python脚本正常执行完毕后的退出状态可能被误判为错误
3. 交互式输入处理在某些终端环境下可能有问题

**解决方案**：

#### 方案1: 使用修复后的脚本
```bash
# 使用修复后的 run_cleaner.sh（已移除 set -e）
bash run_cleaner.sh --info

# 或者使用简化版脚本
./simple_cleaner.sh
```

#### 方案2: 直接使用Python脚本
```bash
# 直接调用Python脚本，避免Shell脚本问题
python3 cursor_cleaner.py --info
python3 cursor_cleaner.py --full
python3 cursor_cleaner.py --cache-only
python3 cursor_cleaner.py --machine-id-only
```

#### 方案3: 使用快速测试脚本
```bash
# 使用专门的测试脚本
./quick_test.sh
```

### 问题2: 权限错误

**症状**：
- "Permission denied" 错误
- 无法访问某些文件或目录

**解决方案**：
```bash
# 确保脚本有执行权限
chmod +x *.sh

# 如果需要，使用sudo运行（谨慎使用）
sudo python3 cursor_cleaner.py --full
```

### 问题3: Python命令未找到

**症状**：
- "python3: command not found"
- "python: command not found"

**解决方案**：
```bash
# 检查Python安装
which python3
which python

# 如果未安装，安装Python
sudo apt update
sudo apt install python3

# 或者使用系统包管理器安装
```

### 问题4: Cursor进程无法停止

**症状**：
- 脚本报告无法停止Cursor进程
- 清理操作失败

**解决方案**：
```bash
# 手动停止Cursor进程
pkill -f cursor
pkill -f Cursor

# 强制停止
pkill -9 -f cursor

# 检查进程状态
ps aux | grep -i cursor
```

### 问题5: 文件不存在错误

**症状**：
- 某些Cursor文件或目录不存在
- 脚本报告文件未找到

**解决方案**：
这通常是正常的，因为：
- 不同版本的Cursor可能有不同的文件结构
- 某些文件只在特定条件下创建
- 脚本会自动跳过不存在的文件

### 问题6: 备份失败

**症状**：
- 无法创建备份文件
- 备份目录创建失败

**解决方案**：
```bash
# 检查当前目录权限
ls -la

# 手动创建备份目录
mkdir -p cursor_backup

# 检查磁盘空间
df -h
```

## 🔧 调试技巧

### 1. 启用详细输出
```bash
# 使用bash的调试模式
bash -x run_cleaner.sh --info

# 或者
set -x
./run_cleaner.sh --info
```

### 2. 检查脚本语法
```bash
# 检查Shell脚本语法
bash -n run_cleaner.sh

# 检查Python脚本语法
python3 -m py_compile cursor_cleaner.py
```

### 3. 逐步执行
```bash
# 分步执行各个功能
python3 cursor_cleaner.py --info
python3 test_cleaner.py
python3 example_usage.py
```

## 📋 环境检查清单

在报告问题前，请检查以下项目：

- [ ] Python版本 (推荐3.6+)
- [ ] 操作系统类型和版本
- [ ] Cursor是否已安装
- [ ] 脚本文件权限
- [ ] 磁盘空间是否充足
- [ ] 是否有其他安全软件干扰

## 🆘 获取帮助

如果问题仍然存在，请提供以下信息：

1. **系统信息**：
   ```bash
   uname -a
   python3 --version
   ```

2. **错误信息**：
   - 完整的错误输出
   - 执行的具体命令

3. **环境状态**：
   ```bash
   ls -la cursor_cleaner/
   ps aux | grep -i cursor
   ```

4. **测试结果**：
   ```bash
   python3 test_cleaner.py
   ```

## 🔄 重置和恢复

如果需要完全重置：

```bash
# 删除所有生成的文件
rm -rf cursor_backup/
rm -rf __pycache__/

# 重新下载或重新创建项目文件
# 确保所有脚本都有正确的权限
chmod +x *.sh
```

## 📞 联系支持

如果以上解决方案都无法解决问题，请：
1. 收集上述调试信息
2. 创建详细的问题报告
3. 包含重现步骤
