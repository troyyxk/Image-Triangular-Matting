import cv2 as cv
import numpy as np

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


def createBMatrix(bArray):
    bMatrix = [None]*6
    j = 0
    for i in range(len(bMatrix)):
        bMatrix[i] = [None]*4
        curRow = bMatrix[i]
        curRow[0] = 0
        curRow[1] = 0
        curRow[2] = 0
        curRow[j] = 1
        j += 1
        if j >= 3:
            j = 0
        curRow[3] = bArray[i]
    return np.array(bMatrix)


def createCMatrix(cArray, bArray):
    cMatrix = [None]*6

    for i in range(6):
        cMatrix[i] = cArray[i] - bArray[i]

    return np.array(cMatrix)
#########################################


if __name__ == '__main__':

    compA = cv.imread("../test_images/tiny/flowers-compA.jpg")
    c0r, c0g, c0b = compA[:, :, 2], compA[:, :, 1], compA[:, :, 0]
    compB = cv.imread("../test_images/tiny/flowers-compB.jpg")
    c1r, c1g, c1b = compB[:, :, 2], compB[:, :, 1], compB[:, :, 0]
    backA = cv.imread("../test_images/tiny/flowers-backA.jpg")
    b0r, b0g, b0b = backA[:, :, 2], backA[:, :, 1], backA[:, :, 0]
    backB = cv.imread("../test_images/tiny/flowers-backB.jpg")
    b1r, b1g, b1b = backB[:, :, 2], backB[:, :, 1], backB[:, :, 0]

    # Step 1, Initialize the resulting alphaOut and colOut array
    numRows = backA.shape[0]
    numCols = backA.shape[1]
    numRGB = backA.shape[2]

    alphaMatrix = [None] * numRows
    frontMatrix = [None] * numRows

    # Step 2,
    for i in range(numRows):
        alphaMatrix[i] = [None] * numCols
        frontMatrix[i] = [None] * numCols
        for j in range(numCols):
            # Create combined matrix
            cMatrix = createCMatrix(compA[i][j].tolist() + compB[i][j].tolist(),
                                    backA[i][j].tolist() + backB[i][j].tolist())
            # Create background Matrix
            bMatrix = createBMatrix(
                backA[i][j].tolist() + backB[i][j].tolist())

            piBMatrix = np.linalg.pinv(bMatrix)

            # Get the result matrix
            resultMatrix = np.matmul(piBMatrix, cMatrix)

            alphaMatrix[i][j] = resultMatrix[3]
            frontPixel = [None]*3
            for k in range(3):
                frontPixel[k] = resultMatrix[k] / resultMatrix[3]
            frontMatrix[i][j] = frontPixel

    alpha = np.array(alphaMatrix)
    foreground = np.array(frontMatrix)

    cv.imshow("foreground", foreground)
    cv.imshow("alpha", alpha)
    cv.waitKey(0)
