# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:45:13 2018

@author: Kyle
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class HeatStructure():
    """ Holds structure for a heat event. Consists of a list of length 'lanes' that stores time data"""

    def __init__(self, lanes):
        self.data = {}
        for lane in range(lanes):
            self.data[lane] = " "

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
            h = HeatStructure(lanes)
            self.heats.append(h)

    #--------------------------------------------------------------------------------------------------------
    def record_heat(self, times):
        """Stores recorded times for current heat to lanes in current heat object within current event instance"""

        if times[0] is ' ':
            return

        for idx, lane in enumerate(self.heats[counter - 1].data):
            lane = times[idx]

        counter = counter + 1
        if counter > len(self.heats):
            self.messageBox('Event is Finished.\n Please record event Data')
            return

    #--------------------------------------------------------------------------------------------------------
    def record_event(outputFile):
        """Writes all event info, including heats and times, to output file"""

        with open(outputFile, 'a'):
            outputFile.write("-----------------------------")
            outputFile.write("Event {}".format(self.number))
            outputFile.write("{0} {1} {2} {3}".format(self.age, self.gender, self.distance, self.stroke))
            for i in len(self.heats):
                outputFile.write("Heat {0} of {1}:".format(i, len(self.heats)))
                for lane in len(self.heats[i].data):
                    outputFile.write("Lane {0}: {1}".format(lane, self.heats[i].data[lane]))
                outputFile.write(" ")
            outputFile.write("----------------------------")
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