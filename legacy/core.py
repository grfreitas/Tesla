#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 22:08:45 2017

@author: gabsrf
"""

import dbManip
import arduino
import brain

print "#------------------------#"
print "#   Welcome to Automata  #"
print "#------------------------#"

print "-> PostgreSQL Database Connected.\n"

connected = True

arduino.openPort()

while connected:
    
    receivedData = False
    pCommand = dbManip.readDB()
    command = pCommand
    
    while not receivedData:
        
        command = dbManip.readDB()
 
        if command != pCommand:
            receivedData = True
    
    command = ''.join(command[len(command)-1])
    
    print("-> You texted: " + command)
    
    if command.lower() == "desligar":
        connected = False
        dbManip.cleanDB()
        
    else:
        param = brain.textNormalization(command)
        arduino.send(param)
        
arduino.closePort()
print "Cya!"
    
    