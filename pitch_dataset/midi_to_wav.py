# make a Python list of the files in the directory
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
import os
def findfiles(directory):
    objects = os.listdir(directory)  # find all objects in a dir
    
    files = []
    for i in objects:  # check if very object in the folder ...
        if isFile(directory + i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files

def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True

import subprocess
#subprocess.check_output(['ls','-l']) #all that is technically needed...

files_ = findfiles("files/")
print("number of midi files: {}".format(len(files_)))

for file_ in files_:
    name = file_.split(".")[0]
    subprocess.run("fluidsynth -F sounds/{}.wav ~/mgen/Sonatina_Symphonic_Orchestra.sf2 files/{}.mid".format(name,name),shell=True)


