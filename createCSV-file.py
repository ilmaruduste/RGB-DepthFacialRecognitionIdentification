import cv2
import dlib
from pathlib import Path
import os
import csv
import re

#Folder with portrait pictures
directory = "/Users/bodeval/Semester5/Computer_Vision/Project/git2/RGB-DepthFacialRecognitionIdentification/alltogetherOutput"

csvFilePath = "/Users/bodeval/Semester5/Computer_Vision/Project/git2/RGB-DepthFacialRecognitionIdentification/data.csv"


#Delete file
if os.path.isfile(csvFilePath):
    os.remove(csvFilePath)

open(csvFilePath, "x")
#Create file


writer = csv.writer(open(csvFilePath,"a"))

writer.writerow(["nameNumber","pixelValues","usage"])

names = {"Christian":0, "Ilmar":1, "Eslem":2}

#Where all the magic happens
def main(directoryPath):


    files = Path(directoryPath).glob('*')
    numberOfFiles = len(list(files))
    number = 1

    traningDataPercentSize = 50
    
    
    files = Path(directoryPath).glob('*')

    index = 0

    #Do for all files found in directoryPath
    for file in files:


        #Ignore .DS_Store file
        if file.name == '.DS_Store':
            continue
        

        #Get name number
        pre, ext = os.path.splitext(file.name)
        #Remove everyhing but charactors from filename
        pre = re.sub(r'[^a-zA-Z ]+', '', pre)
        #print(pre)
        nameNumber = names[pre]
        #print(nameNumber)


        #Get pixel values
        filePath = directoryPath+"/"+file.name
        img = cv2.imread(filePath,0)
        rows,cols = img.shape
        pixelValues = ""
                
        for i in range(rows):
            for j in range(cols):
                pixelValues += str(img[i,j]) + " "

        pixelValues = pixelValues[:-1]

        #Define usage
        usage = ""
        if index < numberOfFiles*(traningDataPercentSize/100):
            #print(index < numberOfFiles*(traningDataPercentSize/100))
            usage = "Training"
        else:
            usage = "Validation"

        #print(usage)
        #print(pixelValues)
        #print("Last value: " + str(pixelValues[-1]))

        #Write

        #pixelValues = ""

        pixels = pixelValues.split(" ")
        
        if len(pixels) != 28900:
            print(len(pixels))
            print(file.name)
        writer.writerow([nameNumber,pixelValues,usage])






def runner():

    main(directory)


runner()









