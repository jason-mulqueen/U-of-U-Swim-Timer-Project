# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:45:13 2018

@author: Kyle
"""
import PyQt5.QtWidgets as qw

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class HeatStructure():
    """ Holds structure for a heat event. Consists of a list of length 'lanes' that stores time data"""

    def __init__(self, lanes):
        self.data = []
        for lane in range(lanes):
            self.data.append(" ")

    def lane(n):
        """Call this function to access lane data in the heat. Basically an indexing tool"""

        return self.data[n]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        
        
class Event():
    "Holds all neccesary info and functions for handling and recording events and included heats."""
    
    def __init__(self, num, age_range, sex, dist, strk, number_of_heats, lane_count):
        self.number   = num
        self.age      = age_range
        self.gender   = sex
        self.distance = dist
        self.stroke   = strk
        self.counter  = 1
        self.lanes    = lane_count

        self.heats    = []
        #Populate heats
        for i in range(int(number_of_heats)):
            h = HeatStructure(self.lanes)
            self.heats.append(h)

    #--------------------------------------------------------------------------------------------------------
    def record_heat(self, times):
        """Stores recorded times for current heat to lanes in current heat object within current event instance"""
        
        blank_time = False
        for idx in range(len(self.heats[self.counter - 1].data)):
            if times[idx] is ' ':
                times[idx] = "No Time Recorded"
                blank_time = True
        if blank_time is True:
            self.messageBox("One or more lanes did not record a time")


        self.heats[self.counter - 1].data[idx] = times[idx]

        self.counter = self.counter + 1
        if self.counter > len(self.heats):
            self.messageBox('Event is Finished.\n Please record event Data')
            return

    #--------------------------------------------------------------------------------------------------------
    def record_event(self, outputFilename):
        """Writes all event info, including heats and times, to output file"""

        with open(outputFilename, "a") as outputFile:
            outputFile.write("-----------------------------\n")
            outputFile.write("Event {}: ".format(self.number))
            outputFile.write("{0} {1} {2} {3}\n".format(self.age, self.gender, self.distance, self.stroke))
            for i in range(len(self.heats)):
                outputFile.write("Heat {0} of {1}:\n".format(i + 1, len(self.heats)))
                for lane in range(len(self.heats[i].data)):
                    outputFile.write("\tLane {0}: {1}\n".format(lane + 1, self.heats[i].data[lane]))
                #outputFile.write(" ")
            outputFile.write("----------------------------\n")
        return
    #--------------------------------------------------------------------------------


    #------------------------------------------------------------
    def messageBox(self, message):
        """Convenient for displaying messages such as errors or relevant info to user"""
        
        msg = qw.QMessageBox()
        msg.setText(message)
        msg.exec_()
#-----------------------------------------------------------------------------------------------------------
            
if __name__ == '__main__':
    heat = HeatStructure(8)
    currentEvent = Event('16-18', 'Mens', '100', 'Butterfly', '3')



# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'event_wizard_real_final.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

####### copied imports may overlap
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper,
        QSize, QTextStream, Qt, QRect,QRegExp, QSortFilterProxyModel)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QInputDialog, QLineEdit,
        QGridLayout, QMdiArea, QMessageBox, QTextEdit, QWidget, QLabel, QComboBox,QPushButton)

from PyQt5.QtWidgets import (QFileDialog, QInputDialog,
        QMdiArea, QMessageBox, QTextEdit, QWidget)

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QLCDNumber, QSlider, QVBoxLayout)
############ end of copied imports

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import (QFileDialog, QInputDialog,
        QMdiArea, QMessageBox, QTextEdit, QWidget)


class Ui_event_wizard(object):
    def print_event_info(self):
        if not self.number_of_heats_combo.currentText():
            self.messageBox("Enter Event Info")
            self.correct_entry = False
            return
        if not self.stroke_combo.currentText():
            self.messageBox("Enter Event Info")
            self.correct_entry = False
            return
        if not self.distance_combo.currentText():
            self.messageBox("Enter Event Info")
            self.correct_entry = False
            return
        if not self.gender_combo.currentText():
            self.messageBox("Enter Event Info")
            self.correct_entry = False
            return
        if not self.age_combo.currentText():
            self.messageBox("Enter Event Info")
            self.correct_entry = False
            return
        if not self.event_number_text_enter.toPlainText():
            self.messageBox("Enter Event Info")
            self.correct_entry = False
            return
        event_number_value = self.event_number_text_enter.toPlainText()
        age_value = self.age_combo.currentText()
        gender_value = self.gender_combo.currentText()
        distance_value = self.distance_combo.currentText()
        stroke_value = self.stroke_combo.currentText()
        number_of_heats_value = self.number_of_heats_combo.currentText()
        with open("event_info.txt","w") as event_info:
            event_info.write(event_number_value + "\n")
            event_info.write(age_value + "\n")
            event_info.write(gender_value + "\n")
            event_info.write(distance_value + "\n")
            event_info.write(stroke_value + "\n")
            event_info.write(number_of_heats_value + "\n")
        self.correct_entry = True
        return
        

    def setupUi_2(self, event_wizard):
        event_wizard.setObjectName("event_wizard")
        event_wizard.resize(650, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(event_wizard.sizePolicy().hasHeightForWidth())
        event_wizard.setSizePolicy(sizePolicy)
        event_wizard.setMaximumSize(QtCore.QSize(650, 200))
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
        event_wizard.setPalette(palette)
        event_wizard.setStyleSheet("\n"
"QToolTip\n"
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
"    color: #FFFFFF;\n"
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
        self.centralwidget = QtWidgets.QWidget(event_wizard)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(200, 10))
        self.label_6.setMaximumSize(QtCore.QSize(10, 200))
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(200, 10))
        self.label_5.setMaximumSize(QtCore.QSize(10, 200))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(200, 10))
        self.label_4.setMaximumSize(QtCore.QSize(10, 200))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(200, 10))
        self.label_3.setMaximumSize(QtCore.QSize(10, 200))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(200, 10))
        self.label_2.setMaximumSize(QtCore.QSize(10, 200))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(200, 0))
        self.label.setMaximumSize(QtCore.QSize(10, 200))
        self.label.setSizeIncrement(QtCore.QSize(0, 0))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.enter_event_information_button = QtWidgets.QPushButton(self.centralwidget)
        self.enter_event_information_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.enter_event_information_button.setObjectName("enter_event_information_button")
        self.gridLayout.addWidget(self.enter_event_information_button, 2, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.event_number_text_enter = QtWidgets.QPlainTextEdit(self.centralwidget)
       

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.event_number_text_enter.sizePolicy().hasHeightForWidth())
        self.event_number_text_enter.setSizePolicy(sizePolicy)

        self.event_number_text_enter.setMinimumSize(QtCore.QSize(200, 40))
        self.event_number_text_enter.setMaximumSize(QtCore.QSize(200, 40))
        self.event_number_text_enter.setStyleSheet("color: rgb(255, 255, 255);")
        self.event_number_text_enter.setObjectName("event_number_text_enter")
        self.horizontalLayout.addWidget(self.event_number_text_enter, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.age_combo = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.age_combo.sizePolicy().hasHeightForWidth())
        self.age_combo.setSizePolicy(sizePolicy)
        self.age_combo.setMinimumSize(QtCore.QSize(200, 10))
        self.age_combo.setMaximumSize(QtCore.QSize(10, 200))
        self.age_combo.setStyleSheet("color: rgb(255, 255, 255);")
        self.age_combo.setObjectName("age_combo")
        self.age_combo.addItem("")
        self.age_combo.setItemText(0, "")
        self.age_combo.addItem("")
        self.age_combo.addItem("")
        self.age_combo.addItem("")
        self.age_combo.addItem("")
        self.age_combo.addItem("")
        self.age_combo.addItem("")
        self.horizontalLayout.addWidget(self.age_combo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.gender_combo = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gender_combo.sizePolicy().hasHeightForWidth())
        self.gender_combo.setSizePolicy(sizePolicy)
        self.gender_combo.setMinimumSize(QtCore.QSize(200, 10))
        self.gender_combo.setMaximumSize(QtCore.QSize(10, 200))
        self.gender_combo.setStyleSheet("color: rgb(255, 255, 255);")
        self.gender_combo.setObjectName("gender_combo")
        self.gender_combo.addItem("")
        self.gender_combo.setItemText(0, "")
        self.gender_combo.addItem("")
        self.gender_combo.addItem("")
        self.gender_combo.addItem("")
        self.gender_combo.addItem("")
        self.horizontalLayout.addWidget(self.gender_combo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.distance_combo = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.distance_combo.sizePolicy().hasHeightForWidth())
        self.distance_combo.setSizePolicy(sizePolicy)
        self.distance_combo.setMinimumSize(QtCore.QSize(200, 10))
        self.distance_combo.setMaximumSize(QtCore.QSize(10, 200))
        self.distance_combo.setStyleSheet("color: rgb(255, 255, 255);")
        self.distance_combo.setObjectName("distance_combo")
        self.distance_combo.addItem("")
        self.distance_combo.setItemText(0, "")
        self.distance_combo.addItem("")
        self.distance_combo.addItem("")
        self.distance_combo.addItem("")
        self.distance_combo.addItem("")
        self.distance_combo.addItem("")
        self.horizontalLayout.addWidget(self.distance_combo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.stroke_combo = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stroke_combo.sizePolicy().hasHeightForWidth())
        self.stroke_combo.setSizePolicy(sizePolicy)
        self.stroke_combo.setMinimumSize(QtCore.QSize(200, 10))
        self.stroke_combo.setMaximumSize(QtCore.QSize(10, 200))
        self.stroke_combo.setStyleSheet("color: rgb(255, 255, 255);")
        self.stroke_combo.setObjectName("stroke_combo")
        self.stroke_combo.addItem("")
        self.stroke_combo.setItemText(0, "")
        self.stroke_combo.addItem("")
        self.stroke_combo.addItem("")
        self.stroke_combo.addItem("")
        self.stroke_combo.addItem("")
        self.stroke_combo.addItem("")
        self.stroke_combo.addItem("")
        self.stroke_combo.addItem("")
        self.horizontalLayout.addWidget(self.stroke_combo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.number_of_heats_combo = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_of_heats_combo.sizePolicy().hasHeightForWidth())
        self.number_of_heats_combo.setSizePolicy(sizePolicy)
        self.number_of_heats_combo.setMinimumSize(QtCore.QSize(200, 10))
        self.number_of_heats_combo.setMaximumSize(QtCore.QSize(10, 200))
        self.number_of_heats_combo.setStyleSheet("color: rgb(255, 255, 255);")
        self.number_of_heats_combo.setObjectName("number_of_heats_combo")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.setItemText(0, "")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.number_of_heats_combo.addItem("")
        self.horizontalLayout.addWidget(self.number_of_heats_combo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        event_wizard.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(event_wizard)
        self.statusbar.setObjectName("statusbar")
        event_wizard.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(event_wizard)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1321, 47))
        self.menuBar.setObjectName("menuBar")
        self.menuOptions = QtWidgets.QMenu(self.menuBar)
        self.menuOptions.setObjectName("menuOptions")
        event_wizard.setMenuBar(self.menuBar)
        self.actionsave_file = QtWidgets.QAction(event_wizard)
        self.actionsave_file.setObjectName("actionsave_file")
        self.actionopen_new_file = QtWidgets.QAction(event_wizard)
        self.actionopen_new_file.setObjectName("actionopen_new_file")
        self.actionAdded_Options = QtWidgets.QAction(event_wizard)
        self.actionAdded_Options.setObjectName("actionAdded_Options")
        self.actionOptions = QtWidgets.QAction(event_wizard)
        self.actionOptions.setObjectName("actionOptions")
        self.actionConfigure_Timers = QtWidgets.QAction(event_wizard)
        self.actionConfigure_Timers.setObjectName("actionConfigure_Timers")
        self.menuOptions.addAction(self.actionConfigure_Timers)
        self.menuBar.addAction(self.menuOptions.menuAction())

        self.retranslateUi_2(event_wizard)
        QtCore.QMetaObject.connectSlotsByName(event_wizard)


    def retranslateUi_2(self, event_wizard):
        _translate = QtCore.QCoreApplication.translate
        event_wizard.setWindowTitle(_translate("event_wizard", "Event Wizard"))
        self.label_6.setText(_translate("event_wizard", "Event Number"))
        self.label_5.setText(_translate("event_wizard", "Age"))
        self.label_4.setText(_translate("event_wizard", "Gender  "))
        self.label_3.setText(_translate("event_wizard", "Distance             "))
        self.label_2.setText(_translate("event_wizard", "Stroke             "))
        self.label.setText(_translate("event_wizard", "Number of Heats"))
        self.enter_event_information_button.setText(_translate("event_wizard", "Enter Event Information"))
        self.age_combo.setItemText(1, _translate("event_wizard", "0-6"))
        self.age_combo.setItemText(2, _translate("event_wizard", "7-8"))
        self.age_combo.setItemText(3, _translate("event_wizard", "9-10"))
        self.age_combo.setItemText(4, _translate("event_wizard", "11-12"))
        self.age_combo.setItemText(5, _translate("event_wizard", "13-14"))
        self.age_combo.setItemText(6, _translate("event_wizard", "15-18"))
        self.gender_combo.setItemText(1, _translate("event_wizard", "Boys"))
        self.gender_combo.setItemText(2, _translate("event_wizard", "Girls"))
        self.gender_combo.setItemText(3, _translate("event_wizard", "Men"))
        self.gender_combo.setItemText(4, _translate("event_wizard", "Women"))
        self.distance_combo.setItemText(1, _translate("event_wizard", "25 yards"))
        self.distance_combo.setItemText(2, _translate("event_wizard", "50 yards"))
        self.distance_combo.setItemText(3, _translate("event_wizard", "100 yards"))
        self.distance_combo.setItemText(4, _translate("event_wizard", "200 yards"))
        self.distance_combo.setItemText(5, _translate("event_wizard", "500 yards"))
        self.stroke_combo.setItemText(1, _translate("event_wizard", "Freestyle"))
        self.stroke_combo.setItemText(2, _translate("event_wizard", "Breaststroke"))
        self.stroke_combo.setItemText(3, _translate("event_wizard", "Butterfly"))
        self.stroke_combo.setItemText(4, _translate("event_wizard", "Backstroke"))
        self.stroke_combo.setItemText(5, _translate("event_wizard", "IM"))
        self.stroke_combo.setItemText(6, _translate("event_wizard", "Medley Relay"))
        self.stroke_combo.setItemText(7, _translate("event_wizard", "Freestlye Relay"))
        self.number_of_heats_combo.setItemText(1, _translate("event_wizard", "1"))
        self.number_of_heats_combo.setItemText(2, _translate("event_wizard", "2"))
        self.number_of_heats_combo.setItemText(3, _translate("event_wizard", "3"))
        self.number_of_heats_combo.setItemText(4, _translate("event_wizard", "4"))
        self.number_of_heats_combo.setItemText(5, _translate("event_wizard", "5"))
        self.number_of_heats_combo.setItemText(6, _translate("event_wizard", "6"))
        self.number_of_heats_combo.setItemText(7, _translate("event_wizard", "7"))
        self.number_of_heats_combo.setItemText(8, _translate("event_wizard", "8"))
        self.number_of_heats_combo.setItemText(9, _translate("event_wizard", "9"))
        self.menuOptions.setTitle(_translate("event_wizard", "Options"))
        self.actionsave_file.setText(_translate("event_wizard", "save file"))
        self.actionopen_new_file.setText(_translate("event_wizard", "open new file"))
        self.actionAdded_Options.setText(_translate("event_wizard", "Added Options"))
        self.actionOptions.setText(_translate("event_wizard", "Options"))
        self.actionConfigure_Timers.setText(_translate("event_wizard", "Configure Timers"))


        #self.enter_event_information_button.clicked.connect(self.print_event_info)
        self.enter_event_information_button.clicked.connect(event_wizard.close)

    def messageBox(self, message):
        """Convenient for displaying messages such as errors or relevant info to user"""
        
        msg = qw.QMessageBox()
        msg.setText(message)
        msg.exec_()
#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    event_wizard = QtWidgets.QMainWindow()
#    ui_event_wizard = Ui_event_wizard()
#    ui_event_wizard.setupUi_2(event_wizard)##
#
#    event_wizard.show()
#    sys.exit(app.exec_())




