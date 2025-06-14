#!/usr/bin/env python3
"""
风车cursorfree1.1l - Cursor编辑器缓存清理工具 GUI版本
支持Windows、macOS和Linux系统
博客地址: https://xoxome.online
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import webbrowser
from cursor_cleaner import CursorCleaner
import sys
import os
from pathlib import Path


class CursorFreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("风车cursorfree1.1l")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置窗口图标（优先使用根目录的logo.ico）
        try:
            # 首先尝试根目录的logo.ico
            root_icon = Path(__file__).parent.parent / "logo.ico"
            local_icon = Path(__file__).parent / "logo.ico"

            if root_icon.exists():
                self.root.iconbitmap(str(root_icon))
            elif local_icon.exists():
                self.root.iconbitmap(str(local_icon))
        except Exception as e:
            # 如果设置图标失败，继续运行程序
            pass
        
        # 创建清理器实例
        self.cleaner = CursorCleaner()
        
        # 创建消息队列用于线程间通信
        self.message_queue = queue.Queue()
        
        # 创建界面
        self.create_widgets()
        
        # 启动消息处理
        self.process_queue()
        
    def create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题和博客链接
        self.create_header(main_frame)
        
        # 功能按钮区域
        self.create_buttons(main_frame)
        
        # 日志显示区域
        self.create_log_area(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """创建标题和博客链接区域"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(header_frame, text="风车cursorfree1.1l", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 博客链接
        blog_frame = ttk.Frame(header_frame)
        blog_frame.grid(row=0, column=1, sticky=tk.E)
        
        blog_label = ttk.Label(blog_frame, text="博客地址: ")
        blog_label.grid(row=0, column=0)
        
        blog_link = ttk.Label(blog_frame, text="https://xoxome.online", 
                             foreground="blue", cursor="hand2")
        blog_link.grid(row=0, column=1)
        blog_link.bind("<Button-1>", self.open_blog)
        
        # 副标题
        subtitle_label = ttk.Label(header_frame, text="Cursor编辑器缓存清理工具", 
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
    def create_buttons(self, parent):
        """创建功能按钮区域"""
        button_frame = ttk.LabelFrame(parent, text="清理选项", padding="10")
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        button_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # 按钮样式
        button_style = {"width": 15, "padding": 5}
        
        # 显示信息按钮
        self.info_btn = ttk.Button(button_frame, text="显示信息", 
                                  command=self.show_info, **button_style)
        self.info_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # 重置机器码按钮
        self.machine_id_btn = ttk.Button(button_frame, text="重置机器码", 
                                        command=self.reset_machine_id, **button_style)
        self.machine_id_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # 清理缓存按钮
        self.cache_btn = ttk.Button(button_frame, text="清理缓存", 
                                   command=self.clean_cache, **button_style)
        self.cache_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # 完整清理按钮
        self.full_btn = ttk.Button(button_frame, text="完整清理", 
                                  command=self.full_clean, **button_style)
        self.full_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # 清空日志按钮
        self.clear_btn = ttk.Button(button_frame, text="清空日志", 
                                   command=self.clear_log, **button_style)
        self.clear_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # 打开备份目录按钮
        self.backup_btn = ttk.Button(button_frame, text="打开备份目录",
                                    command=self.open_backup_dir, **button_style)
        self.backup_btn.grid(row=1, column=1, padx=5, pady=5)

        # 清理备份文件按钮
        self.clean_backup_btn = ttk.Button(button_frame, text="清理备份文件",
                                          command=self.clean_backup_files, **button_style)
        self.clean_backup_btn.grid(row=1, column=2, padx=5, pady=5)

        # 运行测试按钮
        self.test_btn = ttk.Button(button_frame, text="运行测试",
                                  command=self.run_test, **button_style)
        self.test_btn.grid(row=1, column=3, padx=5, pady=5)

        # 关于按钮
        self.about_btn = ttk.Button(button_frame, text="关于",
                                   command=self.show_about, **button_style)
        self.about_btn.grid(row=2, column=0, padx=5, pady=5)
        
    def create_log_area(self, parent):
        """创建日志显示区域"""
        log_frame = ttk.LabelFrame(parent, text="操作日志", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加欢迎信息
        self.log_message("欢迎使用风车cursorfree1.1l！")
        self.log_message("博客地址: https://xoxome.online")
        self.log_message("请选择需要执行的操作。")
        self.log_message("-" * 50)
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(1, weight=1)
        
        # 进度条
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 状态标签
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.grid(row=0, column=1, sticky=tk.W)
        
    def log_message(self, message, level="INFO"):
        """添加日志消息"""
        self.message_queue.put(("log", message, level))
        
    def update_status(self, status):
        """更新状态"""
        self.message_queue.put(("status", status))
        
    def set_buttons_state(self, state):
        """设置按钮状态"""
        self.message_queue.put(("buttons", state))
        
    def process_queue(self):
        """处理消息队列"""
        try:
            while True:
                msg_type, *args = self.message_queue.get_nowait()
                
                if msg_type == "log":
                    message, level = args
                    timestamp = self.cleaner.log.__defaults__[0] if hasattr(self.cleaner, 'log') else ""
                    
                    # 根据级别设置颜色
                    if level == "ERROR":
                        color = "red"
                    elif level == "WARNING":
                        color = "orange"
                    elif level == "SUCCESS":
                        color = "green"
                    else:
                        color = "black"
                    
                    # 插入消息
                    self.log_text.insert(tk.END, f"{message}\n")
                    self.log_text.see(tk.END)
                    
                elif msg_type == "status":
                    status = args[0]
                    self.status_label.config(text=status)
                    
                elif msg_type == "buttons":
                    state = args[0]
                    buttons = [self.info_btn, self.machine_id_btn, self.cache_btn,
                              self.full_btn, self.test_btn, self.clean_backup_btn]
                    for btn in buttons:
                        btn.config(state=state)
                    
                    if state == "disabled":
                        self.progress.start()
                    else:
                        self.progress.stop()
                        
        except queue.Empty:
            pass
        
        # 继续处理队列
        self.root.after(100, self.process_queue)

    def open_blog(self, event):
        """打开博客链接"""
        webbrowser.open("https://xoxome.online")

    def show_info(self):
        """显示Cursor信息"""
        def run():
            self.set_buttons_state("disabled")
            self.update_status("正在获取Cursor信息...")
            self.log_message("=== 显示Cursor信息 ===")

            # 重定向cleaner的日志输出
            original_log = self.cleaner.log
            self.cleaner.log = self.log_message

            try:
                self.cleaner.show_cursor_info()
                self.log_message("信息显示完成", "SUCCESS")
            except Exception as e:
                self.log_message(f"显示信息失败: {e}", "ERROR")
            finally:
                self.cleaner.log = original_log
                self.set_buttons_state("normal")
                self.update_status("就绪")

        threading.Thread(target=run, daemon=True).start()

    def reset_machine_id(self):
        """重置机器码"""
        # 确认对话框
        if not messagebox.askyesno("确认操作",
                                  "确定要重置Cursor的机器码吗？\n\n"
                                  "这将生成新的机器ID和设备ID。\n"
                                  "原始文件将自动备份。"):
            return

        def run():
            self.set_buttons_state("disabled")
            self.update_status("正在重置机器码...")
            self.log_message("=== 重置机器码 ===")

            # 重定向cleaner的日志输出
            original_log = self.cleaner.log
            self.cleaner.log = self.log_message

            try:
                success = self.cleaner.machine_id_only_reset()
                if success:
                    self.log_message("机器码重置完成！", "SUCCESS")
                    messagebox.showinfo("操作完成", "机器码重置成功！\n请重启Cursor以使更改生效。")
                else:
                    self.log_message("机器码重置失败", "ERROR")
                    messagebox.showerror("操作失败", "机器码重置失败，请查看日志了解详情。")
            except Exception as e:
                self.log_message(f"重置机器码失败: {e}", "ERROR")
                messagebox.showerror("操作失败", f"重置机器码失败: {e}")
            finally:
                self.cleaner.log = original_log
                self.set_buttons_state("normal")
                self.update_status("就绪")

        threading.Thread(target=run, daemon=True).start()

    def clean_cache(self):
        """清理缓存"""
        # 确认对话框
        if not messagebox.askyesno("确认操作",
                                  "确定要清理Cursor的缓存吗？\n\n"
                                  "这将删除所有缓存文件。"):
            return

        def run():
            self.set_buttons_state("disabled")
            self.update_status("正在清理缓存...")
            self.log_message("=== 清理缓存 ===")

            # 重定向cleaner的日志输出
            original_log = self.cleaner.log
            self.cleaner.log = self.log_message

            try:
                success = self.cleaner.cache_only_clean()
                if success:
                    self.log_message("缓存清理完成！", "SUCCESS")
                    messagebox.showinfo("操作完成", "缓存清理成功！")
                else:
                    self.log_message("缓存清理失败", "ERROR")
                    messagebox.showerror("操作失败", "缓存清理失败，请查看日志了解详情。")
            except Exception as e:
                self.log_message(f"清理缓存失败: {e}", "ERROR")
                messagebox.showerror("操作失败", f"清理缓存失败: {e}")
            finally:
                self.cleaner.log = original_log
                self.set_buttons_state("normal")
                self.update_status("就绪")

        threading.Thread(target=run, daemon=True).start()

    def full_clean(self):
        """完整清理"""
        # 确认对话框
        if not messagebox.askyesno("确认操作",
                                  "确定要执行完整清理吗？\n\n"
                                  "这将执行以下操作：\n"
                                  "• 重置机器码和遥测ID\n"
                                  "• 清理缓存目录\n"
                                  "• 清理状态数据库\n"
                                  "• 清理工作区存储\n"
                                  "• 清理日志文件\n\n"
                                  "重要文件将自动备份。"):
            return

        def run():
            self.set_buttons_state("disabled")
            self.update_status("正在执行完整清理...")
            self.log_message("=== 完整清理 ===")

            # 重定向cleaner的日志输出
            original_log = self.cleaner.log
            self.cleaner.log = self.log_message

            try:
                success = self.cleaner.full_clean()
                if success:
                    self.log_message("完整清理完成！", "SUCCESS")
                    messagebox.showinfo("操作完成",
                                      "完整清理成功！\n\n"
                                      "请重启Cursor以使更改生效。\n"
                                      f"备份文件保存在: {self.cleaner.backup_dir}")
                else:
                    self.log_message("完整清理失败", "ERROR")
                    messagebox.showerror("操作失败", "完整清理失败，请查看日志了解详情。")
            except Exception as e:
                self.log_message(f"完整清理失败: {e}", "ERROR")
                messagebox.showerror("操作失败", f"完整清理失败: {e}")
            finally:
                self.cleaner.log = original_log
                self.set_buttons_state("normal")
                self.update_status("就绪")

        threading.Thread(target=run, daemon=True).start()

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("日志已清空")

    def open_backup_dir(self):
        """打开备份目录"""
        backup_dir = Path("cursor_backup")
        if backup_dir.exists():
            try:
                if sys.platform.startswith('linux'):
                    os.system(f'xdg-open "{backup_dir.absolute()}"')
                elif sys.platform.startswith('darwin'):
                    os.system(f'open "{backup_dir.absolute()}"')
                elif sys.platform.startswith('win'):
                    os.system(f'explorer "{backup_dir.absolute()}"')
                self.log_message(f"已打开备份目录: {backup_dir.absolute()}")
            except Exception as e:
                self.log_message(f"打开备份目录失败: {e}", "ERROR")
                messagebox.showerror("操作失败", f"打开备份目录失败: {e}")
        else:
            messagebox.showinfo("提示", "备份目录不存在，请先执行清理操作。")

    def clean_backup_files(self):
        """清理备份文件"""
        backup_dir = Path("cursor_backup")

        if not backup_dir.exists():
            messagebox.showinfo("提示", "备份目录不存在，无需清理。")
            return

        # 获取备份目录大小信息
        total_size = 0
        file_count = 0
        try:
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.exists():
                        total_size += file_path.stat().st_size
                        file_count += 1
        except Exception:
            pass

        # 格式化大小显示
        if total_size < 1024:
            size_str = f"{total_size} B"
        elif total_size < 1024 * 1024:
            size_str = f"{total_size / 1024:.1f} KB"
        else:
            size_str = f"{total_size / (1024 * 1024):.1f} MB"

        # 确认对话框
        if not messagebox.askyesno("确认删除",
                                  f"确定要删除所有备份文件吗？\n\n"
                                  f"备份目录: {backup_dir.absolute()}\n"
                                  f"文件数量: {file_count} 个文件\n"
                                  f"占用空间: {size_str}\n\n"
                                  f"⚠️ 此操作不可恢复！"):
            return

        def run():
            self.set_buttons_state("disabled")
            self.update_status("正在清理备份文件...")
            self.log_message("=== 清理备份文件 ===")

            try:
                import shutil

                # 删除整个备份目录
                shutil.rmtree(backup_dir)

                self.log_message(f"已删除备份目录: {backup_dir.absolute()}", "SUCCESS")
                self.log_message(f"清理了 {file_count} 个文件，释放 {size_str} 空间", "SUCCESS")
                self.log_message("备份文件清理完成！", "SUCCESS")

                messagebox.showinfo("清理完成",
                                  f"备份文件清理成功！\n\n"
                                  f"清理了 {file_count} 个文件\n"
                                  f"释放了 {size_str} 空间")

            except Exception as e:
                self.log_message(f"清理备份文件失败: {e}", "ERROR")
                messagebox.showerror("清理失败", f"清理备份文件失败: {e}")
            finally:
                self.set_buttons_state("normal")
                self.update_status("就绪")

        threading.Thread(target=run, daemon=True).start()

    def run_test(self):
        """运行测试"""
        def run():
            self.set_buttons_state("disabled")
            self.update_status("正在运行测试...")
            self.log_message("=== 运行功能测试 ===")

            try:
                # 导入测试模块
                import test_cleaner

                # 重定向输出
                import io
                import contextlib

                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    success = test_cleaner.run_all_tests()

                # 获取测试输出
                test_output = output.getvalue()
                for line in test_output.split('\n'):
                    if line.strip():
                        self.log_message(line)

                if success:
                    self.log_message("所有测试通过！", "SUCCESS")
                    messagebox.showinfo("测试完成", "所有功能测试通过！")
                else:
                    self.log_message("部分测试失败", "WARNING")
                    messagebox.showwarning("测试完成", "部分测试失败，请查看日志了解详情。")

            except ImportError:
                self.log_message("未找到测试模块", "ERROR")
                messagebox.showerror("测试失败", "未找到test_cleaner.py文件")
            except Exception as e:
                self.log_message(f"运行测试失败: {e}", "ERROR")
                messagebox.showerror("测试失败", f"运行测试失败: {e}")
            finally:
                self.set_buttons_state("normal")
                self.update_status("就绪")

        threading.Thread(target=run, daemon=True).start()

    def show_about(self):
        """显示关于对话框"""
        about_text = """风车cursorfree1.1l

Cursor编辑器缓存清理工具 GUI版本

功能特性:
• 重置机器码和遥测ID
• 清理缓存目录
• 清理状态数据库
• 清理工作区存储
• 清理日志文件
• 自动备份重要文件
• 清理备份文件（释放空间）
• 支持Windows、macOS和Linux

博客地址: https://xoxome.online

版本: 1.1l
开发语言: Python + Tkinter"""

        messagebox.showinfo("关于 风车cursorfree1.1l", about_text)


def main():
    """主函数"""
    # 检查依赖
    try:
        from cursor_cleaner import CursorCleaner
    except ImportError:
        messagebox.showerror("错误", "未找到cursor_cleaner.py文件，请确保文件在同一目录下。")
        return

    # 创建主窗口
    root = tk.Tk()

    # 设置主题（如果支持）
    try:
        style = ttk.Style()
        # 尝试使用更现代的主题
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
    except:
        pass

    # 创建应用
    app = CursorFreeGUI(root)

    # 设置窗口关闭事件
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出风车cursorfree1.1l吗？"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    main()
