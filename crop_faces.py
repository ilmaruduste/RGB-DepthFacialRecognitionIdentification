import cv2
import dlib
from pathlib import Path
import os


#Folder with portrait pictures
directory = "/Users/bodeval/Semester5/Computer_Vision/Project/training_data/test/alltogether2"
#Folder so same the cropped faces
outputFolder="/Users/bodeval/Semester5/Computer_Vision/Project/training_data/test/alltogetherOutput"
#The filetype of the new images
filetype=".jpg"
#The final size of the a image in [X,Y]
finalSize=[170,170]

def calculateAverageScale(directory):
    
    detector = dlib.get_frontal_face_detector()

    files = Path(directory).glob('*')
    
    numberOfFiles = 0
    averageScale = 0
    for file in files:
        #Ignore .DS_Store file
        if file.name == '.DS_Store':
            continue
        filePath = directory+"/"+file.name
        img = cv2.imread(filePath)
        # Convert image into grayscale
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        # Use detector to find faces
        faces = detector(gray)

        for face in faces:
            x1 = face.left() # left point
            y1 = face.top() # top point
            x2 = face.right() # right point
            y2 = face.bottom() # bottom point

        print(len(faces))

        if len(faces) != 1:
            continue
        numberOfFiles += 1

        scale_percent = scaleOfRectangle(x1,x2,y1,y2,img)
        averageScale += scale_percent
        print("Number of files: " + str(numberOfFiles))
        print("Average scale: " + str(averageScale))
    averageScale = averageScale/numberOfFiles

    return averageScale

# Takes the size of the face/rectancle and compares it to the full image size. The average scale of x any y is returned.  
def scaleOfRectangle(x1,x2,y1,y2,img):
    current_x_scale = ((x2-x1)/img.shape[1])
    current_y_scale = ((y2-y1)/img.shape[0])
    scale = (current_x_scale+current_y_scale)/2
    return scale


#Where all the magic happens
def main(directoryPath,averageScale):

    files = Path(directoryPath).glob('*')
    number = 1

    #Do for all files found in directoryPath
    for file in files:
        filePath = directoryPath+"/"+file.name

        print("Filename: " + file.name)

        #Ignore .DS_Store file
        if file.name == '.DS_Store':
            continue

        #Get faces with dettector
        detector = dlib.get_frontal_face_detector()
        img = cv2.imread(filePath)
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            x1 = face.left() # left point
            y1 = face.top() # top point
            x2 = face.right() # right point
            y2 = face.bottom() # bottom point

        #Use file if picture only one face is present
        if len(faces) != 1:
            continue
        
        #Calculate a scale given the face size and the img 
        scale = scaleOfRectangle(x1,x2,y1,y2,img)

        #Calculate scaling_factor
        scaling_factor = averageScale/scale

        #Up scale or down scale depending on scale_percent value
        def scale(input):
            return int(input*scaling_factor)

        #Scale the image to make it the same as the average scale
        width = scale(img.shape[1])
        height = scale(img.shape[0])
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        
        #Scale faces coordinates
        for face in faces:
            x1 = scale(x1)
            y1 = scale(y1)
            x2 = scale(x2)
            y2 = scale(y2)
        #Is rectangle of face our of the picture?
        if x1 < 0 or x2 < 0 or y1 <0 or y2 < 0:
            print("Rectangle out of picture")
            continue
        
        #Ignore files with more or less than 1 face in the image
        if len(faces) != 1:
            continue    
        
        #Cut image with scaled values
        img = img[y1:y2, x1:x2]

        height, width, channels = img.shape
        print("Height, width, channels")
        print(height, width, channels)
        print("Scale factor:")
        print(scaling_factor)
        print("Average scale")
        print(averageScale)

        #Cut to make all pictures the same size
        img = img[0:finalSize[0], 0:finalSize[1]]

        #Output files in the outputfolder with a given filetype. Uses the same filename
        pre, ext = os.path.splitext(file.name)
        cv2.imwrite(str(outputFolder)+"/"+pre+filetype, img)

        height, width, channels = img.shape
        print("NEW: Height, width, channels")
        print(height, width, channels)
        print("\n")

        number += 1

def runner():

    #Multiplies all the scales of the faces compared to images, with a face in it and makes an average of that
    averageScale = calculateAverageScale(directory)

    main(directory, averageScale)

    cv2.waitKey(delay=0)
    cv2.destroyAllWindows()

runner()









