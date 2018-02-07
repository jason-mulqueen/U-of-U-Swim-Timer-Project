import os

workingDirectory = os.path.join("C:\\Users", os.getlogin(), "Documents", "Swim Manager")

#This block handles the creation of the specified working directory for compatibility between systems
try:
    os.chdir(workingDirectory)
except FileNotFoundError:
    os.mkdir(workingDirectory)
    os.chdir(workingDirectory)

workingFile     = "heat_info.txt"
filePath        = os.path.join(workingDirectory, workingFile)

with open(filePath, 'w') as outputFile:
    outputFile.write("Something is working")