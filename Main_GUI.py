import PyQt5.QtWidgets as qw
import time
import sys

class Timing_GUI(qw.QWidget):
    """ This class is the main timing GUI for the entire project. """

    def __init__(self, ard):
        super().__init__()
        self.title = "Basic Timing GUI"
        self.initUI()
        self.data = 0
        self.arduino = ard
        self.lane = 0
    
    def initUI(self):
        """ Initializes the GUI elements. Called at GUI startup. """
        numberOfLanes = 2

        self.setWindowTitle(self.title)
        
        layout = qw.QVBoxLayout()
        button = qw.QPushButton("Go!")
        layout.addWidget(button)

        label2 = qw.QLabel("Incoming Times:")
        layout.addWidget(label2)
        #Create a list of labels
        self.labels = []
        self.laneFinish = []
        for i in range(numberOfLanes):
            self.labels.append(qw.QLabel(" "))
            layout.addWidget(self.labels[i])
            self.laneFinish.append(False)

        self.button2 = qw.QPushButton("Close Serial Port")
        layout.addWidget(self.button2)
        
        #Bind Events
        button.clicked.connect(self.sendSignal)
        self.button2.clicked.connect(self.closePort)
        
        #Set geometry and layout and show GUI
        self.setGeometry(100, 100, 500, 200)
        self.setLayout(layout)
        self.show()
    #---------------------------------------------------------------------------    
    def sendSignal(self):
        """ Sends start signal to connected Arduino. Then enters a wait state until timing data has been received. """

        self.t1 = time.perf_counter() #This starts a timer for GUI purposes. Independent of actual time data

        #Send go signal to connected Arduino
        self.arduino.write(str.encode("1")) 

        heatFinish = False
        while heatFinish is False:
            heatFinish = self.updateTimes()
            #print("HeatFinish = ", heatFinish)
   
    #-------------------------------------------------------------------

    def updateTimes(self):
        """ Updates any received times and continues GUI clock """
        if self.readTime(): #Returns lane and time for any finishes that have come in
            self.labels[int(self.lane) - 1].setText("Lane " + self.lane + " Finish: " + self.finalTime + " seconds")
            self.laneFinish[int(self.lane) - 1] = True

        t = time.perf_counter() - self.t1
        #print("t = ", t)

        for lane, laneLabel in enumerate(self.labels):
            #print('-----')
            #print("Lane = ", lane)
            #print("LaneFinish = ", self.laneFinish[int(self.lane) - 1])
            #print('-----')
            if self.laneFinish[lane] is False:
                laneLabel.setText("Lane " + str(lane + 1) + ": {:.2f} seconds".format(t))
        qw.QApplication.processEvents() #This forces the GUI to process all the events above. Necessary for some unknown reason
        
        #for item in self.laneFinish:
            #print(item)

        if all(item is True for item in self.laneFinish):
            return True
        else:
            return False

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

            if int(hund) < 10: # A single digit hundreths value will need a '0' appended to the front
                hund = "0" + hund
            self.finalTime      = str(seconds) + "." + str(hund)
            return True
        else:
            return False
    #--------------------------------------------------------
    def closePort(self):
        """ Closes the Port the arduino object is on. This is absolutely necessary to rerun code on the arduino. """

        arduino.close()
        self.button2.setText("Port Closed")
    #--------------------------------------------------------

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    sudoku = Timing_GUI()
    sys.exit(app.exec_())