import PyQt5.QtWidgets as qw
import time
import sys
from Event_Heat_Definitions import Event

class Timing_GUI(qw.QWidget):
    """ This class is the main timing GUI for the entire project. """

    #---------------------------------------------------------------------------------------------------
    def __init__(self, ard):
        """Initialization function for main GUI class. Called on instance creation in main thread"""

        super().__init__() #Calls initialization function for QWidget class this is all built off of
        self.title = "Basic Timing GUI"
        self.arduino = ard

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #THIS NEEDS TO BE INPUT OPTION
        #HARDCODED NOW FOR TESTING PURPOSES WHILE STUFF GETS SORTED
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.currentEvent = Event(12, '11-12', 'Boys', '500', 'Cage Deathmatch', 2, 6)
        # 3 heats, 2 lanes. Try it out yo
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        self.initUI(self.currentEvent.lanes, len(self.currentEvent.heats))
        self.lane = 0
        self.outputFile = "Meet_Output.txt"
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        

    #--------------------------------------------------------------------
    def initUI(self, lane_count, heat_count):
        """ Initializes the GUI elements. Called at GUI startup. """
        

        self.setWindowTitle(self.title)
        
        #Define Layout
        layout = qw.QVBoxLayout()

        #Instantiate button to send START signal
        go_button = qw.QPushButton("Go!")
        layout.addWidget(go_button)

        label2 = qw.QLabel("Incoming Times:")
        layout.addWidget(label2)
        #Create a list of labels for lane info
        self.labels = []
        #Create list of booleans to store heat finish status
        self.laneFinish = []
        for i in range(lane_count):
            self.laneFinish.append(False)

        #Handle dynamic creation of lane & time labels for each lane
        for i in range(lane_count):
            self.labels.append(qw.QLabel(" "))
            layout.addWidget(self.labels[i])
            

        #Might as well create list to record lane times here as well, cuz whynot?????
        self.times = []
        for i in range(lane_count):
            self.times.append(' ')


        #Buttons
        record_heat_button = qw.QPushButton("Record Heat")
        record_event_button = qw.QPushButton("Record Event")
        self.button2 = qw.QPushButton("Close Serial Port")
        #Add buttons to layout
        layout.addWidget(record_heat_button)
        layout.addWidget(record_event_button)
        layout.addWidget(self.button2)
        
        #Bind Events
        go_button.clicked.connect(self.sendSignal)
        record_heat_button.clicked.connect(self.record_heat_GUI)
        record_heat_button.clicked.connect(self.reset_heat_data)
        record_event_button.clicked.connect(self.currentEvent.record_event)
        self.button2.clicked.connect(self.closePort)
        
        #Set geometry and layout and show GUI
        self.setGeometry(100, 100, 500, 200)
        self.setLayout(layout)
        self.show()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #---------------------------------------------------------------------------
    def sendSignal(self):
        """ Sends start signal to connected Arduino. Then enters a wait state until timing data has been received. """

        self.t1 = time.perf_counter() #This starts a timer for GUI purposes. Independent of actual time data

        #Send go signal to connected Arduino
        self.arduino.write(str.encode("1")) 

        #This block is kind've ugly. It traps in the program in a loop checking for and updating time data until the heat finishes
        heatFinish = False
        while heatFinish is False:
            heatFinish = self.updateTimes() #Watches for and updates times. Returns true if heat is finished
            if heatFinish is True:
                self.arduino.write(str.encode("9"))
        return
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    #-------------------------------------------------------------------
    def updateTimes(self):
        """ Records any received times from 'readTime()' and continues GUI clock """

        #Check for and store time data
        if self.readTime(): #Returns lane and time for any finishes that have come in
            self.times[int(self.lane) - 1] = self.finalTime
            self.labels[int(self.lane) - 1].setText("Lane " + self.lane + " Finish: " + self.finalTime + " seconds")
            self.laneFinish[int(self.lane) - 1] = True

        #Update internal clock
        t = time.perf_counter() - self.t1
        #Update time on GUI for any lanes still swimming
        for lane, laneLabel in enumerate(self.labels):
            if self.laneFinish[lane] is False:
                laneLabel.setText("Lane " + str(lane + 1) + ": {:.2f} seconds".format(t))
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

            if int(hund) < 10: # A single digit hundreths value will need a '0' appended to the front
                hund = "0" + hund
            self.finalTime      = str(seconds) + "." + str(hund)
            return True
        else:
            return False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #--------------------------------------------------------
    def reset_heat_data(self):
        """Resets the data structures for recording times and checking for lane finishes in preparation for next heat"""

        for i in range(len(self.times)):
            self.times[i] = ' '
            self.laneFinish[i] = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #--------------------------------------------------------
    def closePort(self):
        """ Closes the Port the arduino object is on. This is absolutely necessary to rerun code on the Arduino. Shouldn't appear
        in final production code most likely however."""

        self.arduino.close()
        self.button2.setText("Port Closed")
        sys.exit()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #--------------------------------------------------------------
    def record_heat_GUI(self):
        """Hack to properly call the Event.record_heat function"""

        self.currentEvent.record_heat(self.times)
        return
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #------------------------------
    def messageBox(self, message):
        """Handy utility for displaying messages"""

        msg = qw.QMessageBox()
        msg.setText(message)
        msg.exec_()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    sudoku = Timing_GUI()
    sys.exit(app.exec_())