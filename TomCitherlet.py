# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:50:30 2020

@author: jparent1
"""

import os,time
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

def protocol(ergo, device = 1) : 

    minutes = 0
    seconds = 30
    step_s = 1
    duration_s = minutes * 60 + seconds

    os.system('')

    print("\nExperiment duration "+str(duration_s)+" s")
    print("press "+str(device)+" to start on device "+str(device))
    test = b'' 
    while test != b'\x1b' :
        if test.decode() == str(device) :
            load = []
            rpm = []
            print("Start of test on device "+str(device)+" : "+str(datetime.now()))
            for i in range(1,duration_s+1,step_s) :
                if ergo.connected : 
                    load.append(ergo.get_load(device))
                    rpm.append(ergo.get_rpm_decimal(device))
                else :
                    load.append(0)
                    rpm.append(0)
                #clear_line()
                prefix = "Test on device "+str(device)+" : "+str(i)+"/"+str(duration_s)+" s"
                result = "\t Load : "+str(load[i-1])+" W"+"\t RPM :" +str(rpm[i-1])+" tr/min" 
                if i == duration_s :
                    prefix = "Test results on device "+str(device)+" : "
                    result = "\tMean load : "+str(mean(load))+" W"+"\t Mean RPM :" +str(mean(rpm))+" tr/min"
                    end = " press "+str(device)+" to re-start or esc to quit"
                    print(prefix+result+end)
                time.sleep(step_s)
            #print("End of test on device "+str(device)+": "+str(datetime.now())+"\n")
            #print("press "+str(device)+" to start on device "+str(device)+" or esc to quit")
        test = getch()
    
    print("Exit protocol on device "+str(device))

if __name__ == '__main__' :
    import sys
    from threading import Thread
    args = sys.argv
    del args[0] #remove script path form arg list
    threads = []
    ergo = lode38k4()
    if args :
        for arg in args :
            print("device : ",arg)
            t = Thread(target=protocol,args=(ergo,arg,))
            t.start()
            threads.append(t)
    else :
        protocol(ergo)

    for thread in threads :
        pass
        #thread.join()

