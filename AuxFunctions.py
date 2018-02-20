import os

def nav_to_directory(workingDirectory, outputFile):
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

def open_python_port():
    """Find connected Arduino and create serial object on connected port"""
    for port in list(serial.tools.list_ports.comports()):
        if 'Arduino' in port.description:
            return serial.Serial(port[0], 9600)

def wait_for_arduino_ready(arduino):
    """Wait for Arduino to be ready to go"""
    while arduino.inWaiting() <= 0:
        continue
    myData = bytes.decode(arduino.readline()) #Read Ready signal to clear it out