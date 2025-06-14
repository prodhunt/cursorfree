@echo off
chcp 65001 >nul
title Cursor编辑器缓存清理工具

echo ========================================
echo Cursor编辑器缓存清理工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

REM 检查脚本文件是否存在
if not exist "cursor_cleaner.py" (
    echo 错误：未找到cursor_cleaner.py文件
    pause
    exit /b 1
)

:menu
echo.
echo 请选择操作：
echo 1. 完整清理（推荐）
echo 2. 仅清理缓存
echo 3. 仅重置机器码
echo 4. 显示Cursor信息
echo 5. 交互式示例
echo 0. 退出
echo.
set /p choice=请输入选择 (0-5): 

if "%choice%"=="0" goto exit
if "%choice%"=="1" goto full_clean
if "%choice%"=="2" goto cache_only
if "%choice%"=="3" goto machine_id_only
if "%choice%"=="4" goto show_info
if "%choice%"=="5" goto interactive
echo 无效选择，请重试！
goto menu

:full_clean
echo.
echo 执行完整清理...
python cursor_cleaner.py --full
goto menu

:cache_only
echo.
echo 执行缓存清理...
python cursor_cleaner.py --cache-only
goto menu

:machine_id_only
echo.
echo 执行机器码重置...
python cursor_cleaner.py --machine-id-only
goto menu

:show_info
echo.
echo 显示Cursor信息...
python cursor_cleaner.py --info
goto menu

:interactive
echo.
echo 启动交互式示例...
python example_usage.py
goto menu

:exit
echo.
echo 感谢使用！
pause
exit /b 0
