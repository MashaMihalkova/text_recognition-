import pytesseract
import cv2
from pdf2image import convert_from_path
import os
import matplotlib.pyplot as plt

import pytesseract
from pytesseract import Output
import cv2
from Recognize import recognzie
from each_table_recognize import *

# Simple image to string
def load_image(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)


def process_image_tesseract(img_path: str):
    img = load_image(img_path)
    text = pytesseract.image_to_string(img, lang='rus')
    p = img_path[:-4]
    with open(img_path[:-4] + '.txt', 'a+') as f:
        f.write(str(text))
    return text

# def convert_img_to_txt(img_path:str):
#     text = process_image_tesseract(img_path)
#     with open(PATH_TO_SAVE + img_path[-4] + '.txt', 'a+') as f:
#         f.write(str(text))
#     print(text)

def convert_pdf_to_txt(PATH_TO_PYTESSERACT, PATH_TO_PDF, PATH_TO_POPPLER, PATH_TO_SAVE):
    pdfs = PATH_TO_PDF
    pages = convert_from_path(pdfs, 350, poppler_path=PATH_TO_POPPLER)
    i = 1
    for page in pages:
        image_name = PATH_TO_SAVE + "Page_" + str(i) + '.png'
        page.save(image_name, "png")
        tess_text = process_image_tesseract(image_name)
        # with open("D:\\work2\\recognition_text\\otchet\\Page_"+str(i)+'.txt', 'a+') as f:
        # with open(PATH_TO_SAVE + "Page_" + str(i) + '.txt', 'a+') as f:
        #     f.write(str(tess_text))
        print(tess_text)
        i = i + 1

def recognize_list(path):

    rec_file = recognzie(path, r"D:\\work2\\recognition_text\\Tesseract-OCR_rus\\tesseract.exe")
    print(rec_file)
    with open(path[:-4] + '.txt', 'a+') as f:
        f.write(str(rec_file))
    # result.append([list, rec_file, ''])


PATH_TO_PYTESSERACT = "D:\\work2\\recognition_text\\Tesseract-OCR_rus\\tesseract"
PATH_TO_PDF = "D:\\work2\\recognition_text\\otchet\\lists.pdf"
PATH_TO_IMG = "D:\\work2\\recognition_text\\otchet\\small_otch_ (1).png"
PATH_TO_POPPLER = "D:\\work2\\recognition_text\\poppler-0.68.0_x86\\poppler-0.68.0\\bin"
PATH_TO_SAVE = "D:\\work2\\recognition_text\\test_img\\"
PATH_TO_FOLDER = "D:\\work2\\recognition_text\\test_img\\"

pytesseract.pytesseract.tesseract_cmd = PATH_TO_PYTESSERACT
# recognize_list(PATH_TO_IMG)




# h, w, _ = img.shape # assumes color image
#
# # run tesseract, returning the bounding boxes
# boxes = pytesseract.image_to_boxes(img) # also include any config options you use
#
# # draw the bounding boxes on the image
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
#
# # show annotated image and wait for keypress
# cv2.imshow(PATH_TO_IMG, img)
# cv2.imwrite(PATH_TO_SAVE+"box.png",img)
# cv2.waitKey(0)




target_word = "продолжительность"
target_word_end = "бригадир"
COLOR_GREY = 'color'
FILTER = 'THRESH_BINARY+THRESH_OTSU'
# THRESH_OTSU, THRESH_BINARY+THRESH_OTSU, equalizeHist, createCLAHE
for _, _, files in os.walk(PATH_TO_FOLDER):
    for file in files:
        if file[-4:] == '.png' or file[-4:] == '.jpg' or file[-5:] == '.jpeg':
        # if file["extension"] == '.png' or file[-4:] == '.jpg' or file[-5:] == '.jpeg':
            img = cv2.imread(PATH_TO_FOLDER + '/' + file)
            d = pytesseract.image_to_data(img, output_type=Output.DICT, lang='rus')

            word_occurences = [i for i, word in enumerate(d["text"]) if word.lower() == target_word]
            word_occurences_end = [i for i, word in enumerate(d["text"]) if word.lower() == target_word_end]
            image_copy = img.copy()
            for occ in word_occurences:
                # извлекаем ширину, высоту, верхнюю и левую позицию для обнаруженного слова
                w = d["width"][occ]
                h = d["height"][occ]
                l = d["left"][occ]
                t = d["top"][occ]

                #
                # # определяем все точки окружающей рамки
                # p1 = (l-15, t-15)
                # p2 = (1650, t-15)
                # p3 = (1650, 2330)
                # p4 = (l-15, 2330)
                #
                # # рисуем 4 линии (прямоугольник)
                # image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
                # image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
                # image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
                # image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)
                # y: y + h, x: x + w
                if word_occurences_end == []:
                    image_copy = image_copy[t - 25:image_copy.shape[0], l - 25:image_copy.shape[1]]
                    plt.imsave(PATH_TO_FOLDER + f"small_{file}", image_copy)

                    process_image_tesseract(PATH_TO_FOLDER + f"small_{file}")
                    recogn_table(PATH_TO_FOLDER + f"small_{file}", color_grey=COLOR_GREY, filter=FILTER)
                    break

                else:
                    for end_ in word_occurences_end:
                        w_end_ = d["width"][end_]
                        h_end_ = d["height"][end_]
                        l_end_ = d["left"][end_]
                        t_end_ = d["top"][end_]

                        image_copy = image_copy[t - 25:t_end_, l - 25:image_copy.shape[1]]
                        plt.imsave(PATH_TO_FOLDER + f"small_{file}", image_copy)

                        process_image_tesseract(PATH_TO_FOLDER + f"small_{file}")
                        recogn_table(PATH_TO_FOLDER + f"small_{file}", color_grey=COLOR_GREY, filter=FILTER)

                        break
                    break




            # plt.imsave(PATH_TO_FOLDER+"one_world_rect.png", image_copy)
            # for i in range(n_boxes):
            #     (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            #     # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #     text = d['text'][i]
            #     # print(text)
            #     if text == "Продолжительность":
            #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #         print(d['text'][i])
            #
            #
            # cv2.imshow('img', img)
            # cv2.imwrite(PATH_TO_FOLDER+"rect.png", img)
            # cv2.waitKey(0)





# # pdf
# convert_pdf_to_txt(PATH_TO_PYTESSERACT, PATH_TO_PDF, PATH_TO_POPPLER, PATH_TO_SAVE)
#
# # img
# process_image_tesseract(PATH_TO_IMG)

# folder
# for _, _, files in os.walk(PATH_TO_FOLDER):
#     for file in files:
#         print(PATH_TO_FOLDER + '/' + file)
#         if file[-4:] == ".pdf":
#             try:
#                 p = '{}{}\\'.format(PATH_TO_FOLDER, file[:-4])
#                 os.mkdir(p)
#             except OSError:
#                 print('не удалось создать папку {}\\{}\\'.format(PATH_TO_FOLDER, file))
#
#             convert_pdf_to_txt(PATH_TO_PYTESSERACT, PATH_TO_FOLDER + '\\' + file, PATH_TO_POPPLER,
#                                '{}{}\\'.format(PATH_TO_FOLDER, file[:-4]))
#         elif file[-4:] == ".png" or file[-4:] == ".jpg" or file[-5:] == ".jpeg":
#             process_image_tesseract(PATH_TO_FOLDER + '\\' + file)
