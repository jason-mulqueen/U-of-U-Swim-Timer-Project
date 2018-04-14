#Import default libraries
import serial
import serial.tools.list_ports
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import os


#Import custom libraries and classes
#from Main_GUI import Timing_GUI
from Main_GUI import Ui_MainWindow
import AuxFunctions as AF
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Navigate to working directory, creating if necessary
AF.nav_to_directory(os.path.join("C:\\Users", os.getlogin(), "Documents", "Swim Manager"), 'Meet_Output.txt')

#Ready serial device
arduino = AF.open_python_port()
#AF.wait_for_arduino_ready(arduino)


#Run GUI
#app = QApplication(sys.argv)
#sudoku = Timing_GUI(arduino)
#sys.exit(app.exec_())

app = QApplication(sys.argv)
ui = Ui_MainWindow(arduino)
sys.exit(app.exec_())