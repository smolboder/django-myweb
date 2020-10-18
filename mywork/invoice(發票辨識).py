import cv2 as cv
import numpy as np
import pytesseract


def predict(pic):
    """使用opencv 擷取發票號碼的部分"""
    img1 = pic
    # 更改圖片大小
    img1 = cv.resize(img1, (400, 600), interpolation=cv.INTER_CUBIC)

    # # 顯示圖片

    # 去噪
    img = cv.fastNlMeansDenoisingColored(img1, None, 10, 10, 17, 17)
    coefficients = [0, 1, 1]
    m = np.array(coefficients).reshape((1, 3))
    img = cv.transform(img, m)
    # 二值化
    img = cv.GaussianBlur(img, (11, 11), 0)
    img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
    # ret, img = cv.threshold(img, 200, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # 字變細
    kernel = np.ones((3, 1), np.uint8)
    img = cv.erode(img, kernel, iterations=1)

    # 顯示結果

    # 文字拉伸 會變成一塊 設定16 會變成長方形
    ele = cv.getStructuringElement(cv.MORPH_RECT, (100, 1))
    img = cv.dilate(img, ele, iterations=16)
    # # 顯示圖片

    # 找框框
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    # 選取辨識目標

    # 矩形四點座標
    try:
        num = -4
        a = max(contours[num][:, :, 1])[0]
        b = min(contours[num][:, :, 1])[0]
        c = max(contours[num][:, :, 0])[0]
        d = min(contours[num][:, :, 0])[0]
    except:
        num = -1
        a = max(contours[num][:, :, 1])[0]
        b = min(contours[num][:, :, 1])[0]
        c = max(contours[num][:, :, 0])[0]
        d = min(contours[num][:, :, 0])[0]
    # 圖片切片
    img1 = img1[b-5:a+5, d:c]
    # 顯示圖片
    pre_img=img1
    # 辨識目標去噪
    img1 = cv.fastNlMeansDenoisingColored(img1, None, 10, 10, 21, 17)
    coefficients = [0, 1, 1]
    m = np.array(coefficients).reshape((1, 3))
    img1 = cv.transform(img1, m)
    # 二值化
    img1 = cv.GaussianBlur(img1, (5, 5), 0)
    img1 = cv.adaptiveThreshold(img1, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 13)
    # 上下各加黑長條 增加圖片長度 以利辨識
    a = np.full((5, img1.shape[1]), 0).astype('uint8')
    img1 = np.vstack([a, img1, a])  # numpy資料合併
    # # 顯示圖片

    # tesseract文字辨識
    # pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
    text = pytesseract.image_to_string(img1,lang='eng')
    # 顯示辨識結果
    text=text.replace(' ','')
    return text,pre_img

