import PyQt5.QtWidgets as qw
import time
import sys
from Event_Heat_Definitions import Event

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper,
        QSize, QTextStream, Qt, QRect,QRegExp, QSortFilterProxyModel)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QInputDialog, QLineEdit,
        QGridLayout, QMdiArea, QMessageBox, QTextEdit, QWidget, QLabel, QComboBox,QPushButton)

from PyQt5.QtWidgets import (QFileDialog, QInputDialog,
        QMdiArea, QMessageBox, QTextEdit, QWidget)

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QLCDNumber, QSlider, QVBoxLayout, QTextEdit)

#import Event_Wizard
from Event_Heat_Definitions import Ui_event_wizard

class Ui_MainWindow(QMainWindow):
    #####################
    #Create some universal stuff for compatibility

    def launch_Main(self):
        userLaneCount = int(self.comboBox.currentText())
        self.w = QtWidgets.QMainWindow()
        self.setupUi(self.w, userLaneCount)
        self.w.show()

    def __init__(self, ard):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(800, 250))  
        self.move(200,200)
        self.setWindowTitle("Enter the Number of Lanes") 
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)

        

        self.arduino = ard
 
        # Create combobox and add items.
        self.label_lane_enter = QLabel('Enter Number of Lanes',centralWidget)
        self.label_lane_enter.setGeometry(QRect(250, 10, 300, 40))
        self.comboBox = QComboBox(centralWidget)
        self.lane_enter_pushbutton = QPushButton('Enter',centralWidget)
        self.comboBox.setGeometry(QRect(350, 80, 100, 40))
        self.lane_enter_pushbutton.setGeometry(QRect(200, 140, 400, 40))
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("1")
        self.comboBox.addItem("2")
        self.comboBox.addItem("3")
        self.comboBox.addItem("4")
        self.comboBox.addItem("5")
        self.comboBox.addItem("6")
        self.comboBox.addItem("7")
        self.comboBox.addItem("8")
        self.lane_enter_pushbutton.clicked.connect(self.launch_Main)
        self.lane_enter_pushbutton.clicked.connect(self.openWindow)
        self.lane_enter_pushbutton.clicked.connect(self.print_lanes)
        self.show()



        #self.setupUi(QMainWindow())
        #Bind Events
        




    #def print_screen_resolution(self):
    #    screen = app.primaryScreen()
    #    size = screen.size()
    #    print('Your Screen Resolution is: %d x %d' % (size.width(), size.height()))

    def print_lanes(self):
        lane_value = self.comboBox.currentText()
        print("Entered Number of Lanes is:",lane_value)
        self.close()

    def get_event_info(self):
        with open("event_info.txt","r") as event_info_output:
            info = event_info_output.readlines()
            event_number = info[0].strip()
            age = info[1].strip()
            gender = info[2].strip()
            distance = info[3].strip()
            stroke = info[4].strip()
            number_of_heats = info[5].strip()

        self.entered_event_number_main_text.setText(event_number)
        self.entered_age_main_text.setText(age)
        self.entered_gender_main_text.setText(gender)
        self.entered_distance_main_text.setText(distance)
        self.entered_stroke_main_text.setText(stroke)
        self.entered_number_of_heats_main_text.setText(number_of_heats)
        del self.currentEvent
        #print(self.currentEvent.age)
        self.currentEvent = Event(event_number, age, gender, distance, stroke, int(number_of_heats), int(self.lane_count))
        print(self.currentEvent.number)
        print(self.currentEvent.age)
        print(self.currentEvent.gender)
        print(self.currentEvent.distance)
        print(self.currentEvent.stroke)
        print(self.currentEvent.lanes)
        print("Counter =", self.currentEvent.counter)


    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_event_wizard()
        self.ui.setupUi_2(self.window)
        self.ui.enter_event_information_button.clicked.connect(self.get_event_info)
        self.window.show()


    def setupUi(self, MainWindow, lane_count):
        self.times_running = False
        self.currentEvent = Event("Void", "Void", "Void", "Void", "Void", 0, 0)
        self.lane_count = lane_count
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(1100, 900))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 29, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 29, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 29, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 29, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 29, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 29, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet("QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #ffa02f;\n"
"     padding: 1px;\n"
"     border-radius: 3px;\n"
"     opacity: 100;\n"
"}\n"
"\n"
"QWidget\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #171D51;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background: transparent;\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #212121,\n"
"        stop:0.4 #343434/*,\n"
"        stop:0.2 #343434,\n"
"        stop:0.1 #ffaa00*/\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #404040;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"}\n"
"\n"
"QWidget:focus\n"
"{\n"
"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #1e1e1e;\n"
"    border-style: solid;\n"
"    border-radius: 6;\n"
"    padding: 3px;\n"
"    font-size: 12px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    selection-background-color: #ffaa00;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:/down_arrow.png);\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"QCheckBox:disabled\n"
"{\n"
"color: #414141;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #242424;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the tool bar */\n"
"     background: url(:/images/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #d7801a;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #ffaa00;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"}\n"
"\n"
"QCheckBox::indicator{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
"{\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(:/images/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #444;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QtCore.QSize(175, 0))
        self.label_15.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_2.addWidget(self.label_15, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QtCore.QSize(157, 0))
        self.label_14.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_2.addWidget(self.label_14, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(168, 0))
        self.label_13.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_2.addWidget(self.label_13, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(168, 0))
        self.label_12.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(170, 0))
        self.label_11.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_2.addWidget(self.label_11, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(50, 0))
        self.label_10.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
       
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
    
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
      
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
       
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_7.setObjectName("label_7")
      
        self.label_x = QtWidgets.QLabel(self.centralwidget)
        self.label_x.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label_x.setObjectName("label")
        
        #######################
        #Dynamic Lane Labeling
        #######################
        self.labels = [self.label_3, self.label_2, self.label_4,
                       self.label_6, self.label_8, self.label_5,
                       self.label_7, self.label_x]
        for i in range(lane_count):
            self.verticalLayout_3.addWidget(self.labels[i])
        #######################
        self.gridLayout.addLayout(self.verticalLayout_3, 4, 0, 1, 1)
        self.go_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_button.sizePolicy().hasHeightForWidth())
        self.go_button.setSizePolicy(sizePolicy)
        self.go_button.setStyleSheet("color: rgb(255, 255, 255);font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 16pt \"MS Shell Dlg 2\";")
        self.go_button.setObjectName("go_button")



        ###################################################################################
        #Create a list of labels for lane info
        
        self.ledits = []
        #Handle dynamic creation of lane & time labels for each lane
        for i in range(lane_count):
            self.ledits.append(qw.QLineEdit(self.centralwidget))
            

        #Create list of booleans to store heat finish status
        self.laneFinish = []
        for i in range(lane_count):
            self.laneFinish.append(False)
        
       
        #Might as well create list to record lane times here as well, cuz whynot?????
        self.times = []
        for i in range(lane_count):
            self.times.append(' ')
        #####################################################################################
        self.gridLayout.addWidget(self.go_button, 5, 1, 1, 3, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        

        for idx, ledit in enumerate(self.ledits):
            ledit.setSizePolicy(sizePolicy)
            ledit.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
            ledit.setObjectName("lane_" + str(idx) + "_time")
            ledit.setAlignment(QtCore.Qt.AlignRight)
            self.verticalLayout_2.addWidget(ledit, 0, QtCore.Qt.AlignLeft)

        sizePolicy.setHeightForWidth(self.ledits[0].sizePolicy().hasHeightForWidth())
        self.gridLayout.addLayout(self.verticalLayout_2, 4, 1, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem)
        self.record_heat_button = QtWidgets.QPushButton(self.centralwidget)
        self.record_heat_button.setStyleSheet("color: rgb(255, 255, 255);font: 12pt \"MS Shell Dlg 2\";")
        self.record_heat_button.setObjectName("record_heat_button")
        self.verticalLayout_4.addWidget(self.record_heat_button)
        self.create_new_event_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_new_event_button.setStyleSheet("color: rgb(255, 255, 255);font: 12pt \"MS Shell Dlg 2\";")
        self.create_new_event_button.setObjectName("create_new_event_button")
        self.verticalLayout_4.addWidget(self.create_new_event_button)
        
        self.create_new_event_button.clicked.connect(self.openWindow)#opens event wizard
        
        #self.create_new_event_button.clicked.connect(self.print_screen_resolution)
        self.lane_enter_pushbutton.clicked.connect(self.print_lanes)
        self.go_button.clicked.connect(self.sendSignal)
        self.record_heat_button.clicked.connect(self.record_heat_GUI)
        self.record_heat_button.clicked.connect(self.reset_heat_data)
       
        


        self.record_event_button = QtWidgets.QPushButton(self.centralwidget)
        self.record_event_button.setStyleSheet("color: rgb(255, 255, 255);font: 12pt \"MS Shell Dlg 2\";")
        self.record_event_button.setObjectName("record_event")
        self.verticalLayout_4.addWidget(self.record_event_button)
        #self.record_event_button.clicked.connect(self.print_confirmation)
        self.record_event_button.clicked.connect(self.record_event_GUI)
        #self.record_event_button.clicked.connect(self.print_confirmation)

        self.end_meet_button = QtWidgets.QPushButton(self.centralwidget)
        self.end_meet_button.setStyleSheet("color: rgb(255, 255, 255);font: 12pt \"MS Shell Dlg 2\";")
        self.end_meet_button.setObjectName("end_meet_button")
        self.end_meet_button.clicked.connect(self.closePort)
        self.verticalLayout_4.addWidget(self.end_meet_button)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout_4, 4, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.entered_event_number_main_text = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entered_event_number_main_text.sizePolicy().hasHeightForWidth())
        self.entered_event_number_main_text.setSizePolicy(sizePolicy)
        self.entered_event_number_main_text.setMinimumSize(QtCore.QSize(40, 0))
        self.entered_event_number_main_text.setMaximumSize(QtCore.QSize(250, 50))
        self.entered_event_number_main_text.setStyleSheet("color: rgb(255, 255, 255);")
        self.entered_event_number_main_text.setObjectName("entered_event_number_main_text")
        self.horizontalLayout.addWidget(self.entered_event_number_main_text, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.entered_age_main_text = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entered_age_main_text.sizePolicy().hasHeightForWidth())
        self.entered_age_main_text.setSizePolicy(sizePolicy)
        self.entered_age_main_text.setMinimumSize(QtCore.QSize(40, 0))
        self.entered_age_main_text.setStyleSheet("color: rgb(255, 255, 255);")
        self.entered_age_main_text.setObjectName("entered_age_main_text")
        self.horizontalLayout.addWidget(self.entered_age_main_text, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.entered_gender_main_text = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entered_gender_main_text.sizePolicy().hasHeightForWidth())
        self.entered_gender_main_text.setSizePolicy(sizePolicy)
        self.entered_gender_main_text.setMinimumSize(QtCore.QSize(50, 0))
        self.entered_gender_main_text.setStyleSheet("color: rgb(255, 255, 255);")
        self.entered_gender_main_text.setObjectName("entered_gender_main_text")
        self.horizontalLayout.addWidget(self.entered_gender_main_text, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.entered_distance_main_text = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entered_distance_main_text.sizePolicy().hasHeightForWidth())
        self.entered_distance_main_text.setSizePolicy(sizePolicy)
        self.entered_distance_main_text.setMinimumSize(QtCore.QSize(50, 0))
        self.entered_distance_main_text.setStyleSheet("color: rgb(255, 255, 255);")
        self.entered_distance_main_text.setObjectName("entered_distance_main_text")
        self.horizontalLayout.addWidget(self.entered_distance_main_text, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.entered_stroke_main_text = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entered_stroke_main_text.sizePolicy().hasHeightForWidth())
        self.entered_stroke_main_text.setSizePolicy(sizePolicy)
        self.entered_stroke_main_text.setMinimumSize(QtCore.QSize(150, 0))
        self.entered_stroke_main_text.setStyleSheet("color: rgb(255, 255, 255);")
        self.entered_stroke_main_text.setText("")
        self.entered_stroke_main_text.setObjectName("entered_stroke_main_text")
        self.horizontalLayout.addWidget(self.entered_stroke_main_text, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.entered_number_of_heats_main_text = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entered_number_of_heats_main_text.sizePolicy().hasHeightForWidth())
        self.entered_number_of_heats_main_text.setSizePolicy(sizePolicy)
        self.entered_number_of_heats_main_text.setMinimumSize(QtCore.QSize(50, 0))
        self.entered_number_of_heats_main_text.setStyleSheet("color: rgb(255, 255, 255);")
        self.entered_number_of_heats_main_text.setObjectName("entered_number_of_heats_main_text")
        self.horizontalLayout.addWidget(self.entered_number_of_heats_main_text, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 4)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(600, 0))
        self.label_9.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1136, 47))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow, lane_count)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.end_meet_button.clicked.connect(MainWindow.close)

    def retranslateUi(self, MainWindow, lane_count):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_15.setText(_translate("MainWindow", "Event Number"))
        self.label_14.setText(_translate("MainWindow", "Age"))
        self.label_13.setText(_translate("MainWindow", "Gender"))
        self.label_12.setText(_translate("MainWindow", "Distance"))
        self.label_11.setText(_translate("MainWindow", "Stroke"))
        self.label_10.setText(_translate("MainWindow", "Heats"))

        for idx in range(lane_count):
            self.labels[idx].setText(_translate("MainWindow", "Lane " + str(idx + 1)))

        self.go_button.setText(_translate("MainWindow", "            Go!            "))
        self.record_heat_button.setText(_translate("MainWindow", "Record Heat"))
        self.create_new_event_button.setText(_translate("MainWindow", "Create New Event"))
        self.record_event_button.setText(_translate("MainWindow", "Record Event"))
        self.end_meet_button.setText(_translate("MainWindow", "End Meet"))
        self.label_9.setText(_translate("MainWindow", "     Current Event Information                                "))

#---------------------------------------------------------------------------
    def sendSignal(self):
        """ Sends start signal to connected Arduino. Then enters a wait state until timing data has been received. """

        print("SENDING START SIGNAL")

        self.t1 = time.perf_counter() #This starts a timer for GUI purposes. Independent of actual time data

        #Send go signal to connected Arduino
        self.arduino.write(str.encode("1"))

        self.times_running   = True
        self.heat_terminated = False
        #This block is kind've ugly. It traps in the program in a loop checking for and updating time data until the heat finishes
        heatFinish = False
        while heatFinish is False:
            if self.heat_terminated is True:
                return

            heatFinish = self.updateTimes() #Watches for and updates times. Returns true if heat is finished
            #if heatFinish is True:
             #   self.arduino.write(str.encode("9"))
        return
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    #-------------------------------------------------------------------
    def updateTimes(self):
        """ Records any received times from 'readTime()' and continues GUI clock """

        #Check for and store time data
        if self.readTime(): #Returns lane and time for any finishes that have come in
            self.times[int(self.lane) - 1] = self.finalTime
            self.ledits[int(self.lane) - 1].setText(self.finalTime)
            self.laneFinish[int(self.lane) - 1] = True

        #Update internal clock
        t = time.perf_counter() - self.t1
        #Update time on GUI for any lanes still swimming
        for lane, ledit in enumerate(self.ledits):
            if self.laneFinish[lane] is False:
                if t//60 >= 1:
                    if (int(t) - 60*(int(t)//60)) < 10:
                        ledit.setText("{0}:".format(int(t//60)) + "0" + "{:.2f}".format(t - 60*int(t//60)))
                    else:
                        ledit.setText("{0}:".format(int(t//60)) + "{:.2f}".format(t - 60*int(t//60)))
                else:
                    ledit.setText("{:.2f}".format(t))
        qw.QApplication.processEvents() #This forces the GUI to process all the events above. Necessary for some unknown reason
        
        #Check for heat completion
        if all(item is True for item in self.laneFinish):
            return True
        else:
            return False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #------------------------------------------------------------
    def readTime(self):
        """ Checks for a time received from connected Arduino.
            Stores time and lane info in class-wide variables and returns true if time was received. """

        if (self.arduino.inWaiting() > 0):
            data = self.arduino.readline()
            data = bytes.decode(data)

            data = data.split()
            self.lane = data[0]
            seconds   = data[1]
            hund      = data[2]

            if int(hund) is 999:
                self.finalTime = "No Swimmer"
                return True

            if int(hund) < 10: # A single digit hundreths value will need a '0' appended to the front
                hund = "0" + hund

            if int(seconds) > 60:
                if (int(seconds) - 60*(int(seconds)//60)) < 10:
                    self.finalTime = str(int(seconds)//60) + ":" + "0" + str(int(seconds) - 60*(int(seconds)//60)) + "." + str(hund)
                else:
                    self.finalTime = str(int(seconds)//60) + ":" + str(int(seconds) - 60*(int(seconds)//60)) + "." + str(hund)
            else:
                self.finalTime     = str(seconds) + "." + str(hund)
            return True
        else:
            return False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def print_confirmation(self):
        print("This action was recognized")
        return

    #--------------------------------------------------------
    def reset_heat_data(self):
        """Resets the data structures for recording times and checking for lane finishes in preparation for next heat"""

        for i in range(len(self.times)):
            self.times[i] = ' '
            self.laneFinish[i] = False
        
        #Clear out serial buffer so any residual time messages don't affect the next heat
        self.arduino.reset_input_buffer()
        self.arduino.reset_output_buffer()

        #Provide confirmation for user by resetting labels to show message
        for ledit in self.ledits:
            ledit.setText("Waiting...")

        self.times_running = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #--------------------------------------------------------
    def closePort(self):
        """ Closes the Port the arduino object is on. This is absolutely necessary to rerun code on the Arduino. Shouldn't appear
        in final production code most likely however."""

        self.arduino.close()
        self.end_meet_button.setText("Port Closed")
        sys.exit()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def record_event_GUI(self, filename):
        self.currentEvent.record_event("Meet_Data.txt")
    #--------------------------------------------------------------
    def record_heat_GUI(self):
        """Hack to properly call the Event.record_heat function"""

        #Don't do anything if no times are running
        if self.times_running is False:
            return

        if not all(item is True for item in self.laneFinish):
            self.heat_terminated = True

        self.arduino.write(str.encode("9"))
        self.currentEvent.record_heat(self.times)
        return
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #------------------------------
    def messageBox(self, message):
        """Handy utility for displaying messages"""
        app = qw.QApplication(sys.argv)
        msg = qw.QMessageBox()
        msg.setText(message)
        msg.exec_()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(arduino)
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())


