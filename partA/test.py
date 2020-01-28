import cv2 as cv
import numpy as np

if __name__ == '__main__':

    compA = cv.imread("../test_images/tiny/flowers-compA.jpg")
    c0r, c0g, c0b = compA[:, :, 2], compA[:, :, 1], compA[:, :, 0]
    compB = cv.imread("../test_images/tiny/flowers-compB.jpg")
    c1r, c1g, c1b = compB[:, :, 2], compB[:, :, 1], compB[:, :, 0]
    backA = cv.imread("../test_images/tiny/flowers-backA.jpg")
    b0r, b0g, b0b = backA[:, :, 2], backA[:, :, 1], backA[:, :, 0]
    backB = cv.imread("../test_images/tiny/flowers-backB.jpg")
    b1r, b1g, b1b = backB[:, :, 2], backB[:, :, 1], backB[:, :, 0]

    # Composite_delta = Composite - Background
    cd0r, cd0g, cd0b = c0r - b0r, c0g - b0g, c0b - b0b
    cd1r, cd1g, cd1b = c1r - b1r, c1g - b1g, c1b - b1b

    # F' = aF, we use pseudo-inverse to find F'
    (height, width) = cd0r.shape
    fprime = np.zeros((height, width, 4))
    foreground = np.zeros((height, width, 3))
    alpha = np.zeros((height, width))
    # The A in Ax = B
    A = np.asarray([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0]])
    for i in range(height):
        for j in range(width):
            A[0, 3] = -b0r[i, j]
            A[1, 3] = -b0g[i, j]
            A[2, 3] = -b0b[i, j]
            A[3, 3] = -b1r[i, j]
            A[4, 3] = -b1g[i, j]
            A[5, 3] = -b1b[i, j]
            A_inverse = np.linalg.pinv(A)
            if i == 0 and j == 0:
                print(np.matmul(A, A_inverse))
            # The B in Ax = B
            B = np.asarray([cd0r[i, j], cd0g[i, j], cd0b[i, j], cd1r[i, j], cd1g[i, j], cd1b[i, j]])
            fprime[i, j] = np.matmul(A_inverse, B)
            alpha[i, j] = fprime[i, j, 3]
            foreground[i, j] = fprime[i, j, 0:3] / alpha[i, j]
    cv.imshow("foreground", foreground)
    cv.imshow("alpha", alpha)
    cv.waitKey(0)



