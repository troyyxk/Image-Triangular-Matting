# CSC320 Winter 2020
# Assignment 1
# (c) Kyros Kutulakos
##
# DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
# AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION
# BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS
# POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
# DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions,
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing
    # algorithms. These images are initialized to None and populated/accessed by
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = {
            'backA': None,
            'backB': None,
            'compA': None,
            'compB': None,
            'colOut': None,
            'alphaOut': None,
            'backIn': None,
            'colIn': None,
            'alphaIn': None,
            'compOut': None,
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self):
        return {
            'backA': {'msg': 'Image filename for Background A Color', 'default': None},
            'backB': {'msg': 'Image filename for Background B Color', 'default': None},
            'compA': {'msg': 'Image filename for Composite A Color', 'default': None},
            'compB': {'msg': 'Image filename for Composite B Color', 'default': None},
        }
    # Same as above, but for the output arguments

    def mattingOutput(self):
        return {
            'colOut': {'msg': 'Image filename for Object Color', 'default': ['color.tif']},
            'alphaOut': {'msg': 'Image filename for Object Alpha', 'default': ['alpha.tif']}
        }

    def compositingInput(self):
        return {
            'colIn': {'msg': 'Image filename for Object Color', 'default': None},
            'alphaIn': {'msg': 'Image filename for Object Alpha', 'default': None},
            'backIn': {'msg': 'Image filename for Background Color', 'default': None},
        }

    def compositingOutput(self):
        return {
            'compOut': {'msg': 'Image filename for Composite Color', 'default': ['comp.tif']},
        }

    # Copy the output of the triangulation matting algorithm (i.e., the
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################

    # Use OpenCV to read an image from a file and copy its contents to the
    # matting instance's private dictionary object. The key
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        image = cv.imread(fileName)
        if image is None:  # on fail
            msg = "Failed to read image with filename: " + fileName + ", key: " + key
        else:  # on success
            success = True
            self._images[key] = image / 255.0
        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63.
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        image = self._images[key]

        retval = cv.imwrite(fileName, image)
        if not retval:
            msg = "Failed to write image with filename: " + fileName + ", key: " + key
        else:
            success = True
        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary
    # ojbect.
    def triangulationMatting(self):
        """
        success, errorMessage = triangulationMatting(self)

        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        compA = self._images["compA"]
        compB = self._images["compB"]
        backA = self._images["backA"]
        backB = self._images["backB"]

        c0r, c0g, c0b = compA[:, :, 2], compA[:, :, 1], compA[:, :, 0]
        c1r, c1g, c1b = compB[:, :, 2], compB[:, :, 1], compB[:, :, 0]
        b0r, b0g, b0b = backA[:, :, 2], backA[:, :, 1], backA[:, :, 0]
        b1r, b1g, b1b = backB[:, :, 2], backB[:, :, 1], backB[:, :, 0]

        # Composite_delta = Composite - Background
        cd0r, cd0g, cd0b = c0r- b0r, c0g - b0g, c0b - b0b
        cd1r, cd1g, cd1b = c1r - b1r, c1g - b1g, c1b - b1b
        # F' = aF, we use pseudo-inverse to find F'
        (height, width, channels) = backA.shape
        foreground = np.zeros((height, width, channels))
        alpha = np.zeros((height, width))

        for i in range(height):
            for j in range(width):
                # The A in Ax = B
                A = np.array([[1, 0, 0, -b0r[i, j]],
                              [0, 1, 0, -b0g[i, j]],
                              [0, 0, 1, -b0b[i, j]],
                              [1, 0, 0, -b1r[i, j]],
                              [0, 1, 0, -b1g[i, j]],
                              [0, 0, 1, -b1b[i, j]]])

                A_inverse = np.linalg.pinv(A)
                # The B in AX = B

                B = np.array([
                    cd0r[i, j],
                    cd0g[i, j],
                    cd0b[i, j],
                    cd1r[i, j],
                    cd1g[i, j],
                    cd1b[i, j]])
                X = np.clip(np.matmul(A_inverse, B).astype(np.float32), 0.0, 1.0)
                # Flip RGB to BGR
                foreground[i, j] = (X[0:3][::-1])
                alpha[i, j] = X[3]
        cv.imshow("my_fore.tif", foreground.astype(np.float32))
        cv.imshow("my_alpha.tif", alpha.astype(np.float32))
        cv.waitKey()
        cv.destroyAllWindows()
        foreground = foreground.astype(np.float32)
        alpha = alpha.astype(np.float32)
        print(foreground.dtype)
        print(alpha.dtype)
        self._images["colOut"] = foreground
        self._images["alphaOut"] = alpha
        success = True
        #########################################

        return success, msg

    def createComposite(self):
        """
        success, errorMessage = createComposite(self)
        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        foreground = self._images['colIn']
        alpha = self._images['alphaIn']
        background = self._images['backIn']

        compOut = foreground + (1 - alpha) * background
        self._images['compOut'] = compOut
        #########################################
        success = True
        return success, msg
