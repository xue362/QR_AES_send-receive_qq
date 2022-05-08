# -*- coding: utf-8 -*-
import QR
import SR
import os
import time
import datetime
import tkinter as tk
from tkinter import ttk

if __name__ == '__main__':
    key, iv, window_name = '-1', '-1', '1'
    try:
        with open('SETTINGS.txt', 'r', encoding='UTF-8') as file:
            f_list = file.readlines()
            key, iv, window_name = f_list[0], f_list[1], f_list[2]
            key = key.replace('\n', '')
            iv = iv.replace('\n', '')
            window_name = window_name.replace('\n', '')
    except:
        pass

    root_window = tk.Tk()
    # 设置窗口title
    root_window.title('QR_Send&Receive_QQ')
    # 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
    root_window.geometry('500x600')
    root_window.iconbitmap('head.ico')
    # 设置主窗口的背景颜色,颜色值可以是英文单词，或者颜色值的16进制数,除此之外还可以使用Tk内置的颜色常量
    root_window["background"] = "#C9C9C9"
    # 添加文本内,设置字体的前景色和背景色，和字体类型、大小
    tk.Label(root_window, text="欢迎您", bg="yellow", fg="red", font=('Times', 20, 'bold')).grid(row=0, column=0)

    text = tk.Text(root_window, width=55, height=35, undo=True, autoseparators=False, wrap='word')
    text.grid(row=1, column=0, rowspan=4, columnspan=4)

    if (key, iv, window_name) == ('-1', '-1', '-1'):
        text.insert(tk.INSERT, '''
配置有误，检查SETTING.txt

只需保证前两行数据合法，分别为
key/密钥   (16位)
iv/偏移量  (16位)

注意编码为UTF-8''')


    def start():
        contents = 'TIME ' + str(datetime.datetime.now()) + '\n\n'
        contents += text.get('1.0', tk.END)
        contents = QR.encrypt(contents, key, iv)
        QR.make_qr(contents)
        time.sleep(0.2)
        SR.send_qr(window_name)


    def begin():
        SR.receive_qr(window_name)
        time.sleep(0.2)
        contents = QR.scan_qr('result.jpg')
        contents = QR.decrypt(contents, key, iv)
        if contents[0:5] != 'TIME ':
            contents = '失败！检查二维码或密钥！'
        text.delete('0.0', tk.END)
        text.insert(tk.INSERT, '解密：\n\n' + contents)


    tk.Button(root_window, text='撤销', command=text.edit_undo).grid(row=4, column=4)
    tk.Button(root_window, text='恢复', command=text.edit_redo).grid(row=4, column=5)
    tk.Button(root_window, text='加密发送', command=start).grid(row=6, column=1)
    tk.Button(root_window, text='接收解密', command=begin).grid(row=6, column=2)

    def refresh_name():
        c_box['value'] = SR.get_all_window_name()
    tk.Button(root_window, text='刷新', command=refresh_name).grid(row=0, column=3)
    c_box = ttk.Combobox(root_window)
    c_box.grid(row=0, column=2)
    c_box['value'] = SR.get_all_window_name()

    def change_name(event):
        global window_name
        window_name = c_box.get()

    c_box.bind("<<ComboboxSelected>>", change_name)

    root_window.mainloop()

    try:
        os.remove('qrcode.png')
        os.remove('result.jpg')
        os.remove('scr.png')
    except:
        pass
