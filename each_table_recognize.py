import pytesseract
import cv2
from pdf2image import convert_from_path
import os
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from pytesseract import Output
import cv2
from Recognize import recognzie


PATH_TO_PYTESSERACT = "D:\\work2\\recognition_text\\Tesseract-OCR_rus\\tesseract"
PATH_TO_PDF = "D:\\work2\\recognition_text\\otchet\\lists.pdf"
PATH_TO_IMG = "D:\\work2\\recognition_text\\otchet\\small_otch_ (12).png"
PATH_TO_POPPLER = "D:\\work2\\recognition_text\\poppler-0.68.0_x86\\poppler-0.68.0\\bin"
PATH_TO_SAVE = "D:\\work2\\recognition_text\\otchet\\"
PATH_TO_FOLDER = "D:\\work2\\recognition_text\\otchet\\"


def sort2(val):  # helper for sorting by y
    return val[1]
pytesseract.pytesseract.tesseract_cmd = PATH_TO_PYTESSERACT
def recogn_table(path_to_img):

    image = cv2.imread(path_to_img)
    # remove color info
    gray_image= image[:,:,0]

    # (1) thresholding image
    ret,thresh_value = cv2.threshold(gray_image,180,255,cv2.THRESH_BINARY_INV)

    # (2) dilating image to glue letter with e/a
    kernel = np.ones((2,2),np.uint8)
    dilated_value = cv2.dilate(thresh_value,kernel,iterations = 1)

    # (3) looking for countours
    contours, hierarchy = cv2.findContours(dilated_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # (4) extracting coordinates and filtering them empirically
    coordinates = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if h> 50 and w>50 and h*w<350000:
            coordinates.append((x,y,w,h))

    recognized_table = row = []
    prev_y = 0
    coordinates.sort() #sort by x
    coordinates.sort(key = sort2) # sort by y
    for coord in coordinates:
        x,y,w,h = coord
        if y>prev_y+5: #new row if y is changed
            recognized_table.append(row)
            row = []
        crop_img = image[y:y+h, x:x+w]
        # cv2.imshow('crop', crop_img)
        # cv2.waitKey()

        recognized_string = pytesseract.image_to_string(crop_img, lang="rus")
        row.append(recognized_string.replace("\n"," "))
        print(recognized_string)
        with open(path_to_img[:-4] + '_table.txt', 'a+') as f:
            f.write(str(recognized_string))

        prev_y = y
    recognized_table