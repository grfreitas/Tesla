#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 01:35:50 2017

@author: gabsrf
"""

import speech_recognition as sr
from dictionary import keyWords

def textNormalization(str):
        
        text = str.split()
        i=0    
        for word in text:
            text[i] = word.replace(',','')
            text[i] = word.replace('\'','')
            #text[i] = word[1:]
            text[i] = word.lower()
            i = i + 1
            
        text = [word for word in text if word in keyWords]
        
        return text
        
def listenToMic():
        
        r = sr.Recognizer()
        
        with sr.Microphone as source:
            print("\nDiga algo!")
            audio = r.listen(source)
        
        try:          
            return r.recognize_google(audio, language = "pt-BR")
            
        except sr.UnknownValueError:
            return "desconhecido"
            
        except sr.RequestError:
            return "desconectado"  