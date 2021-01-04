import cv2 as cv
import os 
import numpy as np
import qrcode
from PIL import Image as IM
import six
# variables
# Colors  >>> BGR Format(BLUE, GREEN, RED)

GREEN = (0,255,0) 
RED = (0,0,255)
BLACK = (0,0,0)
YELLOW =(0,255,255)
WHITE = (255,255,255)
# fonts: 
fonts = cv.FONT_HERSHEY_COMPLEX

# face detector object
haarDetector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

def faceDetection(image):
    
    # converting image into GraySacle image 
    GrayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = haarDetector.detectMultiScale(GrayImage, 1.1)
    for (x, y, h, w) in faces:
        wP= int(w/3.4)
        hP= int(h/3.4)   
        thickness = 10 
        # cv.rectangle(image, (x, y), (x+w, y+h), YELLOW, 2)
        # cv.rectangle(image, (x-wP,y-hP), (x+w+wP,y+h+hP), GREEN, 3 )
        # creating Mask / empty image 
        mask = np.zeros(image.shape, dtype=np.uint8)
        
        # circle center
        cCX =int(x+w/2)
        cCY = int(y+h/2)
        Radius = (wP+int((h/3)))
        # cv.circle(image,(cCX, cCY), Radius, (BLACK), thickness )
        # making Pixel white where face is present 
        
        cv.circle(mask, (cCX, cCY), Radius, (WHITE), cv.FILLED)
        cv.imshow("circle is White", mask)
        # Write orginal image pixel where mask is WHITE
        ROI = cv.bitwise_and(image, mask)
        cv.imshow("Circle Written Image", ROI)
        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
        # croping the rectangle ROI Where Face Lay in the image
        
        results = ROI[y-hP:y+h+hP, x-wP: x+wP+w]
        # Cropping the mask  
        mask = mask[y-hP:y+h+hP, x-wP: x+wP+w]

        # making pixel White where thy are black 
        results[mask==0] = (255,255,255)
        # converting image to from BGR to RGB format
        RGB_Image= cv.cvtColor(results,  cv.COLOR_BGR2RGB )
        # convert image to Pillow image
        pilImage = IM.fromarray(RGB_Image)
        pilImage.size[0]
        # open image in default image Viewer 
        # pilImage.show()

        cv.imshow("result", results)
        cv.imshow("mask", mask)
    return pilImage

# creating directory path 
ImagDir= 'Images'
files = os.listdir(ImagDir)
print(files)
for file in files:
    imgPath = os.path.join(ImagDir, file)
    # Reading Image from directory
    raw = file.split('.')
    Name = raw[0]
    print(raw)
    Image = cv.imread(imgPath)
    # Size of logo 
    logSize= (90,90)
    Logo = faceDetection(Image)
    Logo.thumbnail(logSize)
    # print(Face_Image.size[0])

    QR_Code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    # adding name to qr code 
    QR_Code.add_data(Name)
    # create QR code Image
    QR_Code.make()
    #converting the QR code in RGB Image 
    RGB_QR_Image = QR_Code.make_image().convert("RGB")
    # define the postiion where image is add
    print(RGB_QR_Image.size[0])
    Position = ((RGB_QR_Image.size[0]-Logo.size[0])//2, (RGB_QR_Image.size[1]- Logo.size[1])//2)
   
    # # adding logo to the iamge 
    RGB_QR_Image.paste(Logo, Position)
    RGB_QR_Image.save(f"QR_{Name}.png")
    RGB_QR_Image.show()
    cv.imshow("Image", Image)
    cv.waitKey(0)
    



