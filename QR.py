from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import qrcode
from PIL import Image
from pyzbar import pyzbar
import os


# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text, key, iv):
    key = key.encode('utf-8')
    mode = AES.MODE_CBC
    iv = bytes(iv, encoding='utf-8')
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text, key, iv):
    key = key.encode('utf-8')
    iv = bytes(iv, encoding='utf-8')
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


def make_qr(text):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=10,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    filename = 'qrcode.png'
    img.save(filename)


def scan_qr(file_dir='qrcode.png'):
    im = Image.open(file_dir)
    return pyzbar.decode(im)[0].data.decode("utf-8")