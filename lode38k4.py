# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:53:18 2020

@author: jparent1
"""

import serial #pip install pyserial
from serial.tools import list_ports_windows as ports

timeout = 0.2
baudrate = 38400

class lode38k4 :
    
    def __init__(self,com_port="",devices=(1,)) :

        if com_port == "" :
            port_list = ports.comports()
            print("list of availbale port")
            for port in port_list :
                print("Check "+port.device+" : "+port.description)
                #test connectioon and lode request status command
                self.serial = serial.Serial(str(port.device),timeout=timeout,baudrate=baudrate)
                test = False
                for device in devices : 
                    result = self.check_port(device,silent=False)
                    test = test or result
                if test :
                    break
        else :
            self.serial = serial.Serial(com_port,timeout=timeout,baudrate=baudrate)
            self.check_port(devices[0],silent=False)

    
    def check_port(self,device,silent=False) : 
        try :
            answer = self.get_serial(device)
            if not silent : 
                print("-LODE device "+str(device)+", serial : "+answer)
            #self.connected = True
            return True
        except ValueError :
            if not silent :
                print("-LODE device "+str(device)+" not found ")
            #self.connected = False
            return False
        
    def set_power(self,device,power) :
        command = 'SP{0}'.format(power)
        answer = self.request(device,command)
        
        return self.acq(answer)
    
    def set_torque(self,device,torque) :
        command = 'ST{0}'.format(int(torque*100))
        answer = self.request(device,command)
        
        return self.acq(answer)
    
    def get_status(self,device) :
        command = 'RS'
        answer = self.request(device,command)
        return int(answer)
    
    def get_serial(self,device) :
        command = 'SN'
        answer = self.request(device,command)
        return answer
        
    def get_load(self,device) :
        command  = 'PM'
        answer = self.request(device,command)
        return int(answer)
    
    def get_rpm(self,device) :
        command  = 'RM'
        answer = self.request(device,command)
        return int(answer)
    
    def get_rpm_decimal(self,device):
        command = 'RN'
        answer = self.request(device,command)
        rpm = int(answer)/10
        return rpm
    
    def request(self,device,command) :
        query = '{0},'.format(device)+command+'\r'
        self.serial.write(query.encode('ascii'))
        response =self.serial.readline()
        [device_id,answer] = response.decode('ascii').strip('\r').split(',')
        #if device_id == device :
        #print(device_id,answer)
        return answer
    
    def acq(self,answer) : 
        if answer == '\x06' :
            return 1
        else :
            return 0
        
    def close(self) :
        self.serial.close()

if __name__ == '__main__':
    ergo = lode38k4(devices=(1,2))