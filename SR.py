# -*- coding: utf-8 -*-
import win32gui, win32ui, win32con, win32api
import time
from io import BytesIO
import win32clipboard
from PIL import Image, ImageGrab
import cv2 as cv
from pyzbar import pyzbar as pyzbar


def send_qr(name):
    def send_to_clipboard(clip_type, data_clip):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data_clip)
        win32clipboard.CloseClipboard()

    filepath = './qrcode.png'
    image = Image.open(filepath)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    send_to_clipboard(win32clipboard.CF_DIB, data)
    # 获取窗口句柄
    handle = win32gui.FindWindow(None, name)
    # while 1==1:
    if 1 == 1:
        # 填充消息
        win32gui.SendMessage(handle, 770, 0, 0)
        # 回车发送消息
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)


def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle


def screenshot(name):
    (x1, y1, x2, y2), handle = get_window_pos(name)
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 设为高亮
    win32gui.SetForegroundWindow(handle)
    # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    '''
    hwndDC = win32gui.GetWindowDC(0)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MonitorDev = win32api.EnumDisplayMonitors(None, None)
    w = MonitorDev[0][2][2]
    h = MonitorDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, 'scr.jpg')
    '''
    win32api.keybd_event(win32con.VK_SNAPSHOT, 0)
    time.sleep(0.2)
    im = ImageGrab.grabclipboard()
    im.save("scr.png")


def find_qr():
    img = cv.imread('scr.png')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    x, y, w, h = 0, 0, 0, 0
    for barcode in barcodes:
        # 提取二维码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        # 目标区域y1:y2,x1:x2
    img_dst = gray[y - 5:y + h + 5, x - 5:x + w + 5]
    # 将二维码区域保存
    cv.imwrite('./result.jpg', img_dst)


def receive_qr(name):
    screenshot(name)
    find_qr()
