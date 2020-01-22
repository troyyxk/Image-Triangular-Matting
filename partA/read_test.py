import numpy as np
import scipy.linalg as sp
import cv2 as cv

path = '../test_images/tiny/flowers-backA.jpg'
image = cv.imread(path)
print(image)
