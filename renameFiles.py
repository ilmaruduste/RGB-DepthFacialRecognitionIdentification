from pathlib import Path
from numpy.lib.function_base import append
import os

directory = '/Users/bodeval/Semester5/Computer_Vision/Project/training_data/test/Ilmar'
 
files = Path(directory).glob('*')

def rename(directory,file,num):
    pre, ext = os.path.splitext(file.name)
    name = "Ilmar"
    newFileName = name+str(num)+ext
    #Checker: Outcomment last line and use this:
    print("Change :" + directory + "/" + newFileName)
    print("New file name: " + directory + "/" + file.name)
    os.rename(directory+"/"+file.name, directory+"/"+newFileName)

num = 0
for file in files:

    if file.name == ".DS_Store":
        continue
    rename(directory,file,num)
    num += 1

