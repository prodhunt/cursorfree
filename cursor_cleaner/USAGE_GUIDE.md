# Cursor清理工具使用指南

## 🎉 问题已解决！

经过修复，现在所有功能都可以正常使用了！

## ✅ 可用的功能

### 1. 完整清理（推荐）
- ✅ **状态**: 正常工作
- 🔧 **功能**: 重置机器码 + 清理缓存 + 清理状态数据库 + 清理工作区存储 + 清理日志
- 📝 **使用**: 选项1 或 `python3 cursor_cleaner.py --full`

### 2. 仅清理缓存
- ✅ **状态**: 正常工作
- 🔧 **功能**: 仅清理Cursor缓存目录
- 📝 **使用**: 选项2 或 `python3 cursor_cleaner.py --cache-only`

### 3. 仅重置机器码
- ✅ **状态**: 正常工作（已修复）
- 🔧 **功能**: 仅重置机器码和遥测ID
- 📝 **使用**: 选项3 或 `python3 cursor_cleaner.py --machine-id-only`

### 4. 显示Cursor信息
- ✅ **状态**: 正常工作
- 🔧 **功能**: 显示系统信息和Cursor路径状态
- 📝 **使用**: 选项4 或 `python3 cursor_cleaner.py --info`

## 🚀 推荐使用方式

### 方式1: 使用简化版启动脚本（最简单）
```bash
./simple_cleaner.sh
```
然后选择对应的数字选项。

### 方式2: 直接使用Python脚本（最稳定）
```bash
# 显示信息
python3 cursor_cleaner.py --info

# 完整清理（推荐）
python3 cursor_cleaner.py --full

# 仅重置机器码
python3 cursor_cleaner.py --machine-id-only

# 仅清理缓存
python3 cursor_cleaner.py --cache-only
```

### 方式3: 使用修复后的原始脚本
```bash
bash run_cleaner.sh --info
```

## 🔧 修复的问题

### 原始问题
- ❌ 选项1和3执行时出现"Terminated"错误
- ❌ `pkill -f cursor`命令会杀死脚本自身

### 解决方案
- ✅ 移除了自动停止Cursor进程的功能
- ✅ 改为警告用户手动关闭Cursor
- ✅ 修复了进程检测逻辑
- ✅ 改进了错误处理

## 📋 使用建议

### 最佳实践
1. **手动关闭Cursor**: 运行清理前先关闭Cursor编辑器
2. **选择完整清理**: 推荐使用选项1进行完整清理
3. **检查备份**: 清理后检查`cursor_backup/`目录中的备份文件
4. **重启Cursor**: 清理完成后重启Cursor以使更改生效

### 安全提示
- ✅ 所有重要文件都会自动备份
- ✅ 不存在的文件会被自动跳过
- ✅ 详细的操作日志帮助追踪问题
- ✅ 支持所有主流操作系统

## 🧪 测试验证

所有功能都已通过测试：

```bash
# 运行功能测试
python3 test_cleaner.py
# 结果: 6/6 测试通过

# 测试机器码重置
python3 cursor_cleaner.py --machine-id-only
# 结果: ✅ 机器码重置完成！

# 测试完整清理
python3 cursor_cleaner.py --full
# 结果: ✅ 完整清理成功完成！
```

## 📁 生成的文件

清理过程中会生成：
- `cursor_backup/YYYYMMDD_HHMMSS/` - 备份目录
- `cursor_backup/YYYYMMDD_HHMMSS/storage.json` - 原始机器码备份

## 🆘 如果仍有问题

如果遇到任何问题：

1. **查看详细文档**: `TROUBLESHOOTING.md`
2. **运行测试**: `python3 test_cleaner.py`
3. **检查权限**: `ls -la *.sh`
4. **手动执行**: 直接使用Python命令

## 🎯 总结

现在所有功能都已修复并正常工作：
- ✅ 选项1（完整清理）- 正常
- ✅ 选项2（仅清理缓存）- 正常  
- ✅ 选项3（仅重置机器码）- 已修复，正常
- ✅ 选项4（显示信息）- 正常

您可以安全地使用任何方式来清理Cursor缓存和重置机器码！🎊
