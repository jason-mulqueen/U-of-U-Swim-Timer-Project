# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:45:13 2018

@author: Kyle
"""
class HeatStructure():
    
    def __init__(self, lanes):
        self.data = {}
        for lane in range(lanes):
            self.data[lane] = "null"

    def lane(n):
        return self.data[n]
        
        
class Event():
    
    def __init__(self, num, age_range, sex, dist, strk, number_of_heats):
        self.number = num
        self.age      = age_range
        self.gender   = sex
        self.distance = dist
        self.stroke   = strk
        self.heats    = []
        
        for i in range(int(number_of_heats)):
            heat = HeatStructure(8)
            self.heats.append(heat)

    def recordEvent(outputFile):
        with open(outputFile, 'a'):
            outputFile.write()
        return
            
if __name__ == '__main__':
    heat = HeatStructure(8)
    currentEvent = Event('16-18', 'Mens', '100', 'Butterfly', '3')
    
    
        
        