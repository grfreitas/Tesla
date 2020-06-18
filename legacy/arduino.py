#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 06:56:23 2017

@author: gabsrf
"""

import serial
from dictionary import states, dict

def openPort():
    
    hasConnected = False
    i = 0
    
    while ((hasConnected == False) and (i < 99)):
        
        try:
            global arduino
            arduino = serial.Serial('/dev/ttyACM'+str(i), 9600)
            hasConnected = True
            print ("-> Arduino on Serial Port /dev/ttyACM" + str(i) + " successfully connected.\n")
            return
            
        except Exception:
            print  ("-> Serial Port /dev/ttyACM" + str(i) + " failed to open.")
            i += 1
            print  "-> Trying next door."
            
def closePort():
    
    arduino.close()
    print "Serial Port Closed.\n"
    
    return
            
def send(parameters):
        
    if len(parameters) >= 2:
        
        state = parameters[0]
        device = parameters[1]
        
        
        if state in states[0]:
            message = "1"
            
        elif state in states[1]:
            message = "0"
        
        message = message + dict[device]
        
        arduino.write(message)
        
        return
            
    else: return