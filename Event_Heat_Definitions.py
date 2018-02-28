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
        if times[0] is ' ':
            return

        for idx in range(len(self.heats[self.counter - 1].data)):
            self.heats[self.counter - 1].data[idx] = times[idx]

        self.counter = self.counter + 1
        if self.counter > len(self.heats):
            self.messageBox('Event is Finished.\n Please record event Data')
            return

    #--------------------------------------------------------------------------------------------------------
    def record_event(self):
        """Writes all event info, including heats and times, to output file"""

        with open("Meet_Data.txt", "a") as outputFile:
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