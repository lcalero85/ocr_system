import cv2
import numpy as np
import pytesseract

# path of tesseract binary
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# function for text proccess
def text_proccesing(img, file_path_result):
    # init parameters
    global text
    image = cv2.imread(img)
    path_to_save_file = file_path_result

    # **************convert image to text**************************
    text_result = pytesseract.image_to_string(image)

    # **********clean text*****************************************
    # Delete bad characters
    # Add caracters to delete from string

    bad_chars = ['|.) Sl ','.', '´%', '!', "*", '♀', ':', '´', 'ONG ', '|', '"', '(', ')', '~', '2%', ',', 'ie', 'hola', '4 ',
                 'i lm A', 'Ww', ' a', '‘ a', '-', 'ul ;s', '‘ ', '@\ SE', 'y ', '<a e', ' _ ;', '—_',
                 'i Shih ARRAN MCE IN', '', '”', 'w ', '|.) Sl', 'At iA’', '-@ “~~ ~', '+4', 'Wy —s','da Rtg','At iA’) smi ~','',' Non ']

    # clean string in for
    for i in bad_chars:
        # Replace bad characters
        text = text_result.replace(i, '')

    # save result in txt file
    textfile = open(file_path_result, "w")
    textfile.write(text)
    textfile.close()
