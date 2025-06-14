# Cursor编辑器缓存清理工具

## 📖 项目简介

这是一个用于清理Cursor编辑器缓存和重置机器码的自动化工具，支持Windows、macOS和Linux系统。

## 🎯 功能特性

- ✅ 自动识别操作系统
- ✅ 清理Cursor缓存目录
- ✅ 重置机器码和遥测ID
- ✅ 自动备份重要文件
- ✅ 详细的操作日志
- ✅ 安全的错误处理

## 📁 Cursor编辑器缓存目录和机器码文件位置

### 🖥️ Linux系统

#### 📂 主要目录
```bash
# Cursor用户数据目录
~/.config/Cursor/User/

# Cursor缓存目录
~/.cache/cursor/
```

#### 🔑 关键文件位置

1. **机器码和遥测ID文件**：
   ```bash
   ~/.config/Cursor/User/globalStorage/storage.json
   ```
   - 包含：`telemetry.machineId`、`telemetry.devDeviceId`

2. **状态数据库**：
   ```bash
   ~/.config/Cursor/User/globalStorage/state.vscdb
   ```
   - SQLite数据库，存储应用状态和历史记录

3. **工作区存储**：
   ```bash
   ~/.config/Cursor/User/workspaceStorage/
   ```

4. **扩展缓存**：
   ```bash
   ~/.config/Cursor/User/extensions/
   ~/.cache/cursor/extensions/
   ```

5. **日志文件**：
   ```bash
   ~/.config/Cursor/logs/
   ```

### 🪟 Windows系统

#### 📂 主要目录
```cmd
# Cursor用户数据目录
%APPDATA%\Cursor\User\

# Cursor缓存目录
%LOCALAPPDATA%\cursor\
```

#### 🔑 关键文件
```cmd
# 机器码文件
%APPDATA%\Cursor\User\globalStorage\storage.json

# 状态数据库
%APPDATA%\Cursor\User\globalStorage\state.vscdb

# 工作区存储
%APPDATA%\Cursor\User\workspaceStorage\

# 扩展缓存
%APPDATA%\Cursor\User\extensions\
%LOCALAPPDATA%\cursor\extensions\
```

### 🍎 macOS系统

#### 📂 主要目录
```bash
# Cursor用户数据目录
~/Library/Application Support/Cursor/User/

# Cursor缓存目录
~/Library/Caches/cursor/
```

#### 🔑 关键文件
```bash
# 机器码文件
~/Library/Application Support/Cursor/User/globalStorage/storage.json

# 状态数据库
~/Library/Application Support/Cursor/User/globalStorage/state.vscdb

# 工作区存储
~/Library/Application Support/Cursor/User/workspaceStorage/

# 扩展缓存
~/Library/Application Support/Cursor/User/extensions/
~/Library/Caches/cursor/extensions/
```

## 🔍 重要的缓存文件类型

1. **机器标识文件**：
   - `storage.json` - 包含机器ID和设备ID
   - `state.vscdb` - SQLite数据库，存储应用状态

2. **缓存目录内容**：
   - `CachedExtensions/` - 扩展缓存
   - `logs/` - 日志文件
   - `User/workspaceStorage/` - 工作区特定数据
   - `User/globalStorage/` - 全局存储数据

## 🚀 使用方法

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行脚本
```bash
python cursor_cleaner.py
```

### 命令行参数
```bash
# 完整清理（推荐）
python3 cursor_cleaner.py --full

# 仅清理缓存
python3 cursor_cleaner.py --cache-only

# 仅重置机器码
python3 cursor_cleaner.py --machine-id-only

# 显示Cursor信息
python3 cursor_cleaner.py --info
```

### 启动脚本使用
```bash
# 使用修复后的启动脚本
bash run_cleaner.sh --info

# 使用简化版启动脚本（推荐）
./simple_cleaner.sh

# 使用快速测试脚本
./quick_test.sh
```

## ⚠️ 注意事项

1. **备份重要数据**：清理前建议备份重要的配置和扩展
2. **关闭Cursor**：执行清理前务必完全关闭Cursor编辑器
3. **重新配置**：清理后可能需要重新登录和配置某些设置
4. **管理员权限**：某些操作可能需要管理员权限

## 📝 更新日志

- v1.0.0 - 初始版本，支持基本的缓存清理和机器码重置功能

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具。

## 🛠️ 手动清理命令 (Linux)

如果您想手动清理Cursor缓存，可以使用以下命令：

```bash
# 停止Cursor进程
pkill -f cursor

# 清理缓存目录
rm -rf ~/.cache/cursor/

# 清理特定的机器码文件
rm -f ~/.config/Cursor/User/globalStorage/storage.json
rm -f ~/.config/Cursor/User/globalStorage/state.vscdb

# 清理工作区存储（可选）
rm -rf ~/.config/Cursor/User/workspaceStorage/

# 清理日志（可选）
rm -rf ~/.config/Cursor/logs/
```

## 📋 项目文件结构

```
cursor_cleaner/
├── README.md              # 项目说明文档
├── PROJECT_SUMMARY.md     # 项目总结文档
├── TROUBLESHOOTING.md     # 故障排除指南
├── cursor_cleaner.py      # 主要清理脚本
├── example_usage.py       # 使用示例脚本
├── test_cleaner.py        # 功能测试脚本
├── requirements.txt       # Python依赖包
├── run_cleaner.bat       # Windows启动脚本
├── run_cleaner.sh        # Linux/macOS启动脚本（修复版）
├── simple_cleaner.sh     # 简化版启动脚本（推荐）
├── quick_test.sh         # 快速测试脚本
└── cursor_backup/        # 自动生成的备份目录
```

## 🔧 高级用法

### 在代码中使用

```python
from cursor_cleaner import CursorCleaner

# 创建清理器实例
cleaner = CursorCleaner()

# 显示Cursor信息
cleaner.show_cursor_info()

# 执行完整清理
success = cleaner.full_clean()

# 仅清理缓存
success = cleaner.cache_only_clean()

# 仅重置机器码
success = cleaner.machine_id_only_reset()
```

### 自定义备份目录

```python
from cursor_cleaner import CursorCleaner
from pathlib import Path

cleaner = CursorCleaner()
cleaner.backup_dir = Path("my_custom_backup")
cleaner.full_clean()
```

## 🐛 故障排除

### 常见问题

1. **权限错误**
   - 在Linux/macOS上可能需要sudo权限
   - 确保Cursor已完全关闭

2. **文件不存在**
   - 某些文件可能不存在，这是正常的
   - 脚本会自动跳过不存在的文件

3. **进程无法停止**
   - 手动关闭Cursor编辑器
   - 检查是否有其他Cursor相关进程

### 日志分析

脚本会输出详细的操作日志，包括：
- 操作时间戳
- 操作类型（INFO/WARNING/ERROR）
- 具体操作内容
- 文件路径信息

## 📄 许可证

MIT License
