

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2

import numpy as np
import dlib


from pathlib import Path
from numpy.lib.function_base import append, average
import os

directory = "/Users/bodeval/Semester5/Computer_Vision/Project/training_data/test/alltogether2"

outputFolder="/Users/bodeval/Semester5/Computer_Vision/Project/training_data/test/alltogetherOutput"
filename="picture"
filetype=".jpg"



''' 
path = "/Users/bodeval/Semester5/Computer_Vision/Project/data/Christian/20211123_170932_rgb.png"

img = image.load_img(path)


#cv2.imshow("windowname", img)




import cv2
 
img = cv2.imread(path).shape

print(img)

train = ImageDataGenerator(rescale=1/255)
validation = ImageDataGenerator(rescale=1/255)


train_dataset = train.flow_from_directory("basedata/train/", target_size=(200,200), batch_size=3, label_mode="binary")

validation_dataset = train.flow_from_directory("basedata/train/", target_size=(200,200), batch_size=3, class_mode=3)
 '''
def calculateAverageScale(directory):
    import cv2
    
    detector = dlib.get_frontal_face_detector()

    files = Path(directory).glob('*')
    
    numberOfFiles = 0
    averageScale = 0
    for file in files:
        

        if file.name == '.DS_Store':
            continue
        filePath = directory+"/"+file.name
        img = cv2.imread(filePath)
        # Convert image into grayscale
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

        # Use detector to find landmarks
        faces = detector(gray)


        for face in faces:
            x1 = face.left() # left point
            y1 = face.top() # top point
            x2 = face.right() # right point
            y2 = face.bottom() # bottom point

        print(len(faces))

        if len(faces) != 1:
            continue
        
        

        scale_percent = scaleOfRectangle(x1,x2,y1,y2,img)

        numberOfFiles += 1
        averageScale += scale_percent
        
        print("Number of files: " + str(numberOfFiles))
        print("Average scale: " + str(averageScale))
    averageScale = averageScale/numberOfFiles

    return averageScale


def scaleOfRectangle(x1,x2,y1,y2,img):
    current_x_scale = ((x2-x1)/img.shape[1])
    current_y_scale = ((y2-y1)/img.shape[0])
    scale_percent = (current_x_scale+current_y_scale)/2
    return scale_percent



def main(directoryPath,averageScale):

    files = Path(directoryPath).glob('*')
    number = 1
    for file in files:
        filePath = directoryPath+"/"+file.name

        print(file.name)

        if file.name == '.DS_Store':
            continue
        print(file.name)


        # Load the detector
        detector = dlib.get_frontal_face_detector()

        #path = "/Users/bodeval/Semester5/Computer_Vision/Project/training_data/test/Christian/20211123_170528_rgb.png"


        # read the image
        img = cv2.imread(filePath)

        # Convert image into grayscale
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

        # Use detector to find landmarks
        faces = detector(gray)

        for face in faces:
            x1 = face.left() # left point
            y1 = face.top() # top point
            x2 = face.right() # right point
            y2 = face.bottom() # bottom point
            # Draw a rectangle
            #cv2.rectangle(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)

        if len(faces) != 1:
            continue

        scale_percent = scaleOfRectangle(x1,x2,y1,y2,img)

        scale_percent = averageScale/scale_percent

        def scale(input):
            return int(input*scale_percent)

        width = scale(img.shape[1])
        height = scale(img.shape[0])
        dim = (width, height)

        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        
        img = resized

        #Scale faces coordinates
        for face in faces:
            x1 = scale(x1)
            y1 = scale(y1)
            x2 = scale(x2)
            y2 = scale(y2)
            #cv2.rectangle(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)

        if x1 < 0 or x2 < 0 or y1 <0 or y2 < 0:
            print("Ok")
            continue


        if len(faces) != 1:
            continue    

        # show the image
        #cv2.imshow(winname="Face", mat=img)

        #Center x,y
        #center = [int((x1+x2)/2),int((y1+y2)/2)]
        #Draw point
        #cropped_image = cv2.circle(img, (center[0],center[1]), radius=0, color=(0, 0, 255), thickness=5)

        # Cropping an image
        #cropped_image = img[int(center[1]-size[1]/2):int(center[1]+size[1]/2), int(center[0]-size[0]/2):int(center[0]+size[0]/2)]
        img = img[y1:y2, x1:x2]
        croppedName = "cropped"+str(number)
        #cv2.imshow(croppedName, cropped_image)

        height, width, channels = img.shape
        print("Height, width, channels")
        print(height, width, channels)
        print("Scale percent:")
        print(scale_percent)
        print("Average scale")
        print(averageScale)
        print("")

        

        """ width = 100
        height = 10
        dim = (width, height)
        
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) """

        img = img[0:170, 0:170]



        pre, ext = os.path.splitext(file.name)

        cv2.imwrite(str(outputFolder)+"/"+pre+filetype, img)

        height, width, channels = img.shape
        print("NEW: Height, width, channels")
        print(height, width, channels)

        number += 1

def runner():

    averageScale = calculateAverageScale(directory)

    main(directory, averageScale)




    cv2.waitKey(delay=0)
    # Close all windows
    cv2.destroyAllWindows()

runner()









