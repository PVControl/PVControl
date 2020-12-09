# -*- coding: utf-8 -*-
#"""
#Created on Fri May  1 20:29:13 2020
#
#@author: Migue
#"""
#
import requests
from requests.exceptions import HTTPError
import json
import time
import csv
import subprocess, sys
from Parametros_FV import *
from csvFv import CsvFv

DEBUG = False

if usar_fronius == 0:
        #print (commands.getoutput('sudo systemctl stop srne'))
        print (subprocess.getoutput('sudo systemctl stop fronius'))
        sys.exit()





    
class fronius:

    def __init__(self):
    
        self.dct = {}
        self.cmd_meter = 'http://' + IP_fronius + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi'
        self.cmd_inverter = 'http://' + IP_fronius + '/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData'
        
        
    def read_data_meter(self):
    
        try:
        
            response = requests.get(self.cmd_meter)
            meter = json.loads(response.content)
            Wred = (-1)*float((meter['Body']['Data']['Site']['P_Grid']))
            Consumo = round((-1)*float((meter['Body']['Data']['Site']['P_Load'])),2)
            #print(Wred,Consumo)
            try:
                Wplaca = float((meter['Body']['Data']['Site']['P_PV']))
            except:
                Wplaca = 0
            if DEBUG: print('Wred',Wred,'Consumo',Consumo,'Wplaca',Wplaca)
            
            self.dct['Wred'] = Wred
            self.dct['Consumo'] = Consumo
            self.dct['Wplaca'] = Wplaca
            return self.dct
            
        except:
            
            if DEBUG: print('Error lectura meter')
            return None
            
            
    def read_data_inverter(self):
    
        try:
        
            response = requests.get(self.cmd_inverter)
            inverter = json.loads(response.content)
            print('Vred',inverter)
            Vred = float((inverter['Body']['Data']['UAC']['Value']))
            Vplaca = float((inverter['Body']['Data']['UDC']['Value']))
            #EFF = Pout(AC)/Pin(DC) * 100
            #Pin = Vi * Ii
            Pin = Vplaca * float((inverter['Body']['Data']['IDC']['Value']))
            EFF = ((float((inverter['Body']['Data']['PAC']['Value'])) / Pin) * 100)
            
            if DEBUG: print('Vred',Vred,'Vplaca',Vplaca)
            
            self.dct['Vred'] = Vred
            self.dct['Vplaca'] = Vplaca
            self.dct['EFF'] = EFF
            return self.dct
            
        except:
            
            if DEBUG: print('Error lectura inverter')
            self.dct['Vred'] = 230
            self.dct['Vplaca'] = 0
            return self.dct

if __name__ == '__main__':
    c = CsvFv('/run/shm/datos_fronius.csv') 
    
    while True:
        try:
            ve = fronius()           
            
            datos_inverter = ve.read_data_inverter()
            
            if usar_meter == 1:
                datos_meter = ve.read_data_meter()
                datos_inverter.update(datos_meter)                
                datos_inverter['Ibat'] = datos_meter['Wred']/datos_inverter['Vred']
                datos_inverter['Vbat'] = datos_inverter['Vred']
                datos_inverter['Iplaca'] = datos_meter['Wplaca']/datos_inverter['Vred']
                datos_inverter['Aux1'] = datos_meter['Wred'] + 10000
                Temp = 0
                
            datos= datos_inverter
            
            tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
            tiempo_sg = time.time()
            
            datos['Tiempo'] = tiempo
            datos['Tiempo_sg'] = tiempo_sg
            
            #print(datos)
            if datos != None :
                c.escribirCsv(datos)       
             
            
            time.sleep(5)
            
        except KeyboardInterrupt:   # Se ha pulsado CTRL+C!!
            break
        except:
            #print("error no conocido")
            time.sleep(5)
            #sys.exit()