import cv2
import numpy as np


# function for pre-process the image


def pre_image_proccessing(img, image_path):
    # parameters  image to proccess and path of image proccessed
    # open image for proccesing
    open_image = cv2.imread(img)

    # resize image
    resizeimage = cv2.resize(open_image, (1000, 700))

    # deskew image optional
    gray = cv2.cvtColor(resizeimage, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = resizeimage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(resizeimage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # convert to grayscale
    grayscale_image = cv2.cvtColor(resizeimage, cv2.COLOR_BGR2GRAY)

    # clean image
    clean_image = cv2.medianBlur(grayscale_image, 3)

    # erode image
    kernel = np.ones((2, 2), np.uint8)
    erode_image = cv2.erode(clean_image, kernel, iterations=1)

    # brightness
    beta = 1
    alpha = 1
    brightness = cv2.convertScaleAbs(clean_image, beta=beta, alpha=alpha)

    # contrast
    alpha_contrast = 2.1
    contrast_image = cv2.addWeighted(brightness, alpha_contrast, np.zeros(brightness.shape, brightness.dtype), 0, 0)

    # edge detection image
    canny_image = cv2.Canny(contrast_image, 100, 200)

    # histogram
    # histo_img = cv2.equalizeHist(contrast_image, cv2.COLOR_BGR2GRAY)

    # save in you file system
    proccess_image = contrast_image
    cv2.imwrite(image_path, proccess_image)

    # for debug only
    # cv2.imshow('proccess image', proccess_image)
    # cv2.waitKey(0)
