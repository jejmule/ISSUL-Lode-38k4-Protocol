# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:50:30 2020

@author: jparent1
"""

import time
from msvcrt import getch
from statistics import mean
from datetime import datetime

from attr import s
from lode38k4 import lode38k4

def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)

ergo = lode38k4()

minutes = 0
seconds = 10
step_s = 1
duration_s = minutes * 60 + seconds

print("\nExperiment duration "+str(duration_s)+" s")
print("press any key to start or esc to quit")
test = getch()
while test != b'\x1b' :
    load = []
    rpm = []
    print(print("\nStart of test : "+str(datetime.now())))
    for i in range(1,duration_s+1,step_s) :
        if ergo.connected : 
            load.append(ergo.get_load())
            rpm.append(ergo.get_rpm_decimal())
        else :
            load.append(0)
            rpm.append(0)
        clear_line()
        prefix = "Test running : "+str(i)+"/"+str(duration_s)+" s"
        if i == duration_s :
            prefix = "Test results : "
        print(prefix+"\tMean load : "+str(mean(load))+" W"+"\t Mean RPM :" +str(mean(load))+" tr/min")
        time.sleep(step_s)
    print("End of test : "+str(datetime.now())+"\n")
    print("press any key to start or esc to quit")
    test = getch()

