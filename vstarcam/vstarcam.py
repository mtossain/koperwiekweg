#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:12:19 2015

@author: Michel Tossaint
"""

import urllib

def Setting(IP,Port,User,Pwd,Param,Value):
    StartString = "http://"+IP+":"+str(Port)+"/camera_control.cgi&param="
    StopString = "&user="+User+"&pwd="+Pwd
    CommandStr = StartString+str(Param)+"&value="+str(Value)+StopString
    urllib.urlretrieve(CommandStr)
    print(CommandStr)
    

def Snapshot(IP,Port,User,Pwd,FileName):
    CommandStr = "http://"+IP+":"+str(Port)+"/snapshot.cgi&user="+User+"&pwd="+Pwd
    urllib.urlretrieve(CommandStr, FileName)
    print(CommandStr+ ' ' + FileName)

def PTZ(IP,Port,User,Pwd,Command):
    StartString = "http://"+IP+":"+str(Port)+"/decoder_control.cgi&command="
    StopString = "&user="+User+"&pwd="+Pwd
    
    if Command == 'Up':
        urllib.urlretrieve(StartString+str(0)+StopString)
    if Command == 'UpStop':
        urllib.urlretrieve(StartString+str(1)+StopString)
    if Command == 'Down':
        urllib.urlretrieve(StartString+str(2)+StopString)
    if Command == 'DownStop':
        urllib.urlretrieve(StartString+str(3)+StopString)
    if Command == 'Left':
        urllib.urlretrieve(StartString+str(4)+StopString)
    if Command == 'LeftStop':
        urllib.urlretrieve(StartString+str(5)+StopString)
    if Command == 'Right':
        urllib.urlretrieve(StartString+str(6)+StopString)
    if Command == 'RightStop':
        urllib.urlretrieve(StartString+str(7)+StopString)
    
    if Command == 'Center':
        urllib.urlretrieve(StartString+str(25)+StopString)
    if Command == 'UpDown':
        urllib.urlretrieve(StartString+str(26)+StopString)
    if Command == 'UpDownStop':
        urllib.urlretrieve(StartString+str(27)+StopString)
    if Command == 'LeftRight':
        urllib.urlretrieve(StartString+str(28)+StopString)
    if Command == 'LeftRightStop':
        urllib.urlretrieve(StartString+str(29)+StopString)
    
    if Command == 'SetPreset1':
        urllib.urlretrieve(StartString+str(30)+StopString)
    if Command == 'CallPreset1':
        urllib.urlretrieve(StartString+str(31)+StopString)
    if Command == 'SetPreset2':
        urllib.urlretrieve(StartString+str(32)+StopString)
    if Command == 'CallPreset2':
        urllib.urlretrieve(StartString+str(33)+StopString)
    if Command == 'SetPreset3':
        urllib.urlretrieve(StartString+str(34)+StopString)
    if Command == 'CallPreset3':
        urllib.urlretrieve(StartString+str(35)+StopString)
    if Command == 'SetPreset4':
        urllib.urlretrieve(StartString+str(36)+StopString)
    if Command == 'CallPreset4':
        urllib.urlretrieve(StartString+str(37)+StopString)
    if Command == 'SetPreset5':
        urllib.urlretrieve(StartString+str(38)+StopString)
    if Command == 'CallPreset5':
        urllib.urlretrieve(StartString+str(39)+StopString)
    if Command == 'SetPreset6':
        urllib.urlretrieve(StartString+str(40)+StopString)
    if Command == 'CallPreset6':
        urllib.urlretrieve(StartString+str(41)+StopString)
    if Command == 'SetPreset7':
        urllib.urlretrieve(StartString+str(42)+StopString)
    if Command == 'CallPreset7':
        urllib.urlretrieve(StartString+str(43)+StopString)
    if Command == 'SetPreset8':
        urllib.urlretrieve(StartString+str(44)+StopString)
    if Command == 'CallPreset8':
        urllib.urlretrieve(StartString+str(45)+StopString)
    if Command == 'SetPreset9':
        urllib.urlretrieve(StartString+str(46)+StopString)
    if Command == 'CallPreset9':
        urllib.urlretrieve(StartString+str(47)+StopString)
    if Command == 'SetPreset10':
        urllib.urlretrieve(StartString+str(48)+StopString)
    if Command == 'CallPreset10':
        urllib.urlretrieve(StartString+str(49)+StopString)
    if Command == 'SetPreset11':
        urllib.urlretrieve(StartString+str(50)+StopString)
    if Command == 'CallPreset11':
        urllib.urlretrieve(StartString+str(51)+StopString)
    if Command == 'SetPreset12':
        urllib.urlretrieve(StartString+str(52)+StopString)
    if Command == 'CallPreset12':
        urllib.urlretrieve(StartString+str(53)+StopString)
    if Command == 'SetPreset13':
        urllib.urlretrieve(StartString+str(54)+StopString)
    if Command == 'CallPreset13':
        urllib.urlretrieve(StartString+str(55)+StopString)
    if Command == 'SetPreset14':
        urllib.urlretrieve(StartString+str(56)+StopString)
    if Command == 'CallPreset14':
        urllib.urlretrieve(StartString+str(57)+StopString)
    if Command == 'SetPreset15':
        urllib.urlretrieve(StartString+str(58)+StopString)
    if Command == 'CallPreset15':
        urllib.urlretrieve(StartString+str(59)+StopString)
    if Command == 'SetPreset16':
        urllib.urlretrieve(StartString+str(60)+StopString)
    if Command == 'CallPreset16':
        urllib.urlretrieve(StartString+str(61)+StopString)
        
    if Command == 'LeftUp':
        urllib.urlretrieve(StartString+str(90)+StopString)
    if Command == 'RightUp':
        urllib.urlretrieve(StartString+str(91)+StopString)
    if Command == 'LeftDown':
        urllib.urlretrieve(StartString+str(92)+StopString)
    if Command == 'RightDown':
        urllib.urlretrieve(StartString+str(93)+StopString)

    if Command == 'IOHigh':
        urllib.urlretrieve(StartString+str(94)+StopString)
    if Command == 'IOLow':
        urllib.urlretrieve(StartString+str(95)+StopString)
      
    if Command == 'MotoTest':
        urllib.urlretrieve(StartString+str(255)+StopString)
