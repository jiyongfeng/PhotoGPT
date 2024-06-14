#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-05-23 14:43:54
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-06-14 18:59:21
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import tkinter as tk
from tkinter import filedialog, messagebox

import photo_backup_utils


def select_source_directory():
    """选择源路径"""
    source_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)  # 清空原路径输入框
    source_entry.insert(tk.END, source_path)  # 将选择的原路径显示在输入框中


def select_destination_directory():
    """选择目标路径"""
    destination_path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)  # 清空目标路径输入框
    destination_entry.insert(tk.END, destination_path)  # 将选择的目标路径显示在输入框中


def start_backup():
    """开始备份"""
    source_folder = source_entry.get()  # 获取用户输入的原路径
    destination_folder = destination_entry.get()  # 获取用户输入的目标路径

    selected_types = [jpg_var.get(), bmp_var.get(),
                      png_var.get(), tif_var.get()]

    photo_backup_utils.copy_photos_by_date(
        source_folder, destination_folder, selected_types)
    messagebox.showinfo("备份完成", "照片备份已完成！")


# 创建主窗口
window = tk.Tk()
window.title("照片备份工具")

# 创建选择原路径的按钮和输入框
source_button = tk.Button(window, text="选择原路径",
                          command=select_source_directory)
source_button.pack()
source_entry = tk.Entry(window, width=50)
source_entry.pack()

# 创建选择目标路径的按钮和输入框
destination_button = tk.Button(
    window, text="选择目标路径", command=select_destination_directory)
destination_button.pack()
destination_entry = tk.Entry(window, width=50)
destination_entry.pack()

# 创建备份文件类型勾选框
jpg_var = tk.IntVar()
bmp_var = tk.IntVar()
png_var = tk.IntVar()
tif_var = tk.IntVar()

# 增加描述：请选择要备份的文件类型
label = tk.Label(window, text="请选择要备份的文件类型")
label.pack()
jpg_checkbox = tk.Checkbutton(window, text="jpg", variable=jpg_var)
bmp_checkbox = tk.Checkbutton(window, text="bmp", variable=bmp_var)
png_checkbox = tk.Checkbutton(window, text="png", variable=png_var)
tif_checkbox = tk.Checkbutton(window, text="tif", variable=tif_var)
jpg_checkbox.pack(side=tk.LEFT)
bmp_checkbox.pack(side=tk.LEFT)
png_checkbox.pack(side=tk.LEFT)
tif_checkbox.pack(side=tk.LEFT)

# 增加一行空白
tk.Label(window, height=2).pack()

# 创建开始备份按钮，换行显示
start_backup_button = tk.Button(window, text="开始备份", command=start_backup)
start_backup_button.pack(side=tk.LEFT)


# 运行GUI主循环
window.mainloop()
