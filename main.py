'''
AUTHOR: Asadullah Dal
Company Name: AiPhile
purpose: Youtube Channel 
Channel URL: https://youtube.com/c/aiphile

'''
import PIL
import cv2 as cv
import numpy as np
import qrcode
import os 
from PIL import Image as IM

# Colors 
GREEN = (0,255,0)
RED = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW =( 0, 255,255)

haarDetector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

# Creating face detector Function 

def faceDetection (Image):
    #function Disrcption 
    ''' 
    This Function take image(Mat) as argument, detects face, crop's the circular area of detect face,
    with some padding applied, returns a rectangle area of face with some color filed around the area between circle and rectangle

    :param Image:  Take image(Mat) as only argument

    :return: rectangle with circular face in it.
    '''
    # converting image into GrayScale image  
    grayImage = cv.cvtColor(Image, cv.COLOR_BGR2GRAY)
    # found face are 
    faces = haarDetector.detectMultiScale(grayImage)
    for (x, y, h, w) in faces:
        # adding padding to increase face area 
        wPadding = int(w/3.4)
        hPadding = int(h/3.4)
        LinThickness =1

        """Drawing Normal Rectangle which provided by Opencv ROI of face"""
        # cv.rectangle(Image, (x, y), (x+w, y+h), YELLOW, LinThickness)
        """ Increasing the face area here
        by adding the padding around the orginal ROI of face from right, left, top and bottom, in order
        to crop more area of face """
        # cv.rectangle(Image, (x-wPadding, y-hPadding), (x+w+wPadding, y+h+hPadding), GREEN, 10)
        # creating the empty image using numpy 
        mask = np.zeros(Image.shape, dtype = np.uint8)
        # cv.imshow("empty Mask", mask)
        
        # Circle Parametes 
        # center Point of circle
        cCX = int(x+w/2)
        ccY = int(y+h/2)
        """ Calculating the Radius of Circle"""
        Radius = (wPadding+int(h/2))
        """ Drwaing Circle on the image """
        # cv.circle(Image, (cCX, ccY), Radius, (WHITE),2)
        
        """Creating Circle on the Mask on oder to write image"""
        cv.circle(mask, (cCX, ccY), Radius, (WHITE),cv.FILLED)
        
        " show the Circle filled mask"
        cv.imshow("Filled Circle", mask)
        
        
        # """Writing face area on the Mask using Bitwise_and operator from opnecv""" 
        ROI = cv.bitwise_and(Image, mask)
        "Written face ROI"
        cv.imshow("Faces written on Complete Mask ", ROI)
        # converting mask into GrayScale image 
        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
        
        # croping the max rectangle area 
        cropedRectFace= ROI[y-hPadding: y+h+hPadding, x-wPadding: x+wPadding+w]
        cv.imshow('Cropped Rectangle', cropedRectFace)
        
        # Cropping the mask as well 
        mask = mask[y-hPadding: y+h+hPadding, x-wPadding: x+wPadding+w]
        
        # change the Pixel Color where they are black around face cropped reactangle face in it
        cropedRectFace[mask==0] = YELLOW
   
        cv.imshow("Final Result",cropedRectFace)
    return cropedRectFace 

# Create QRCode Function
# """" 
def CreateQRCode(Logo, data, Version=1):
    #Function Discrption 
    '''
    This Function create a QR code and paste(add) logo in the center of image
    This function tacks three arguments

    :param Logo(image): This image tack PIL image as first argument 
    :param data: data that can be written on the QR code 
    :param Version: this argument by default is one, but you can specify from 1 to 40
     which will define how big the QR code should be, its depends on the data as well 
    '''
    LogoSize = (60,60)
    Logo.thumbnail(LogoSize)

    # Setting parametter of QR Code 
    QR_Code = qrcode.QRCode(
    version=Version,
    error_correction=qrcode.constants.ERROR_CORRECT_H
)   
    data2="https://www.youtube.com/c/aiphile"
    QR_Code.add_data(data)
    # create QR_Code
    QR_Code.make()
    # QR_Code.make_image(fill_color="green", back_color="white")
    #converting the QR code in RGB Image 
    RGB_QR_Image = QR_Code.make_image().convert("RGB")
    # print(RGB_QR_Image.size[0])
    # Define center postion for Logo
    Position = ((RGB_QR_Image.size[0]-Logo.size[0])//2, (RGB_QR_Image.size[1]- Logo.size[1])//2)
   
    # # adding logo to the QR code  
    RGB_QR_Image.paste(Logo, Position)
    # Saving the output image files 
    RGB_QR_Image.save(f"Results\QR_{data}.png")
    # Show image in default Image Viewer 
    # RGB_QR_Image.show()

# Reading all images from directory
ImgDir = 'Images'
fileList = os.listdir(ImgDir)
for file in fileList:
    print(file)
    # CREATING THE IMAGE PATH 
    imgPath = os.path.join(ImgDir, file)
    # READING THE IMAGE FROM DIR 
    matImage = cv.imread(imgPath)
    # CALLING FACE DETECTION FUNCTION 
    Out_image = faceDetection(matImage)
    
    # Converting image color representation from opencv (BGR) to Pillow(RGB) 
    RGB_image = cv.cvtColor(Out_image, cv.COLOR_BGR2RGB)
    
    # converting Opencv image into PILLOW Format 
    PIL_Image = IM.fromarray(RGB_image)

    # Open image into Default image Viewer
    # PIL_Image.show()

    # geting image name without extension 
    FileNames=file.split(".")
    data =FileNames[0]
    # calling the function Create QR code
    CreateQRCode(PIL_Image, data)

    # converting image into Pillow  image format
    # cv.imshow("outPutImage", Out_image)
    cv.imshow("Orginal Image", matImage)
    cv.waitKey(0)

