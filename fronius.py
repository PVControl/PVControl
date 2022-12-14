# -*- coding: utf-8 -*-
#
#Version 30/Oct/22
#

import requests
from requests.exceptions import HTTPError
import json
import time
import subprocess, sys
import MySQLdb 
import multiprocessing

from Parametros_FV import *

DEBUG = False
#Comprobacion argumentos en comando
if '-p' in sys.argv: DEBUG = True # para test .... realiza print en distintos sitios

if sum (usar_fronius) == 0:
    print (subprocess.getoutput('sudo systemctl stop fronius'))
    sys.exit()

import colorama # colores en ventana Terminal
from colorama import Fore, Back, Style
colorama.init()

print (Style.BRIGHT + Fore.YELLOW + 'Arrancando'+ Fore.GREEN +' fronius.py') #+Style.RESET_ALL)
print()


def equipo_lectura (indice):  # como entrada solo el indice del Fronius de las listas definidas en Parametros_FV.py    

    print ('')
    print(Fore.BLUE+'=' *40,f'Proceso {equipo}{indice}  IP= {IP_FRONIUS[indice]}', '=' *40) 
    if indice == 0: N_equipo = ""
    else: N_equipo = f"{indice}"
    print(Fore.CYAN + f'Clave en tabla equipos.... {equipo}{N_equipo}') 
    
    time.sleep(20) # le damos un tiempo inicial para establecer comunicacion antes de lectura
    

    class fronius:

        def __init__(self):
        
            self.dct = {}
            self.cmd_meter = 'http://' + IP_FRONIUS[indice] + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi'
            self.cmd_inverter = 'http://' + IP_FRONIUS[indice] + '/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData'
            #'http://' + IP_FRONIUS + '/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System'  # Meter en tiempo real

        def read_data_meter(self):
        
            try:    
                response = requests.get(self.cmd_meter)
                meter = json.loads(response.content)
                Meter_location = str(meter['Body']['Data']['Site']['Meter_Location']) # respuestas posibles "load", "grid", "unknown"
                Wred = round((-1)*float((meter['Body']['Data']['Site']['P_Grid'])),2)
                Consumo = round((-1)*float((meter['Body']['Data']['Site']['P_Load'])),2)
                if Meter_location == "load":    
                    Wred = Consumo
                try:
                    Wplaca = round(float((meter['Body']['Data']['Site']['P_PV'])),2)
                except:
                    Wplaca = 0
                if DEBUG: print(Fore.GREEN+f'/ METER: Wred={Wred:>6.1f}-Consumo={Consumo:>6.1f}-Wplaca={Wplaca:>6.1f}-Meter_loc={Meter_location}')
                
                self.dct['Wred'] = Wred
                self.dct['Consumo'] = Consumo
                self.dct['Wplaca'] = Wplaca
                self.dct['Meter_location'] = Meter_location 
                return self.dct
                
            except:
                
                if DEBUG: print(Fore.RED+f'Error lectura meter {indice}')
                return None     
                
                
        def read_data_inverter(self):
        
            try:
                ee=10
                response = requests.get(self.cmd_inverter)
                ee=20
                inverter = json.loads(response.content)
                if DEBUG:
                    print(Fore.RESET,inverter)
                    print ('=' *100)
                    
                
                ee=30
                Vred = round(float((inverter['Body']['Data']['UAC']['Value'])),2)
                ee=40
                Ired = round(float((inverter['Body']['Data']['IAC']['Value'])),2)
                ee=50
                Vplaca = round(float((inverter['Body']['Data']['UDC']['Value'])),2)
                ee=60
                Fred = round(float((inverter['Body']['Data']['FAC']['Value'])),2)    
                #EFF = Pout(AC)/Pin(DC) * 100
                #Pin = Vi * Ii
                ee=70
                if Vplaca == None: Vplaca=0
                Pin = Vplaca * float((inverter['Body']['Data']['IDC']['Value']))
                try:
                    EFF = round(((float((inverter['Body']['Data']['PAC']['Value'])) / Pin) * 100),2)
                except:
                    EFF=100
                    pass
                ee=80
                
                self.dct['Vred'] = Vred
                self.dct['Ired'] = Ired
                self.dct['Vplaca'] = Vplaca
                self.dct['EFF'] = EFF
                self.dct['Fred'] = Fred 
                
            except:
                
                if DEBUG: print(Fore.RED+f'Error lectura inverter{indice} - {ee}')
                self.dct['Vred'] = Vred = 230
                self.dct['Vplaca'] = Vplaca = 0
                self.dct['EFF'] = EFF = 100
                self.dct['Fred'] = Fred = 0  
                
            if DEBUG:
                    print(Fore.CYAN+time.strftime("%Y-%m-%d %H:%M:%S")+f': INV{indice}: Vred={Vred:>5.1f}-Vplaca={Vplaca:>5.1f}-Fred={Fred:>5.1f}', end='') 
            
            return self.dct


    db = MySQLdb.connect(host = servidor, user = usuario, passwd = clave, db = basedatos)
    cursor = db.cursor()
            
    while True:
        try:
            t1= time.time()
            ve = fronius()           
            
            datos_inverter = ve.read_data_inverter()
            
            if usar_meter_fronius[indice] == 1:
                datos_meter = ve.read_data_meter()
                datos_inverter.update(datos_meter)                
                datos_inverter['Meter_location'] = (datos_inverter['Meter_location'])
                if datos_inverter['Vred'] != 0:
                    datos_inverter['Ired'] = round(datos_meter['Wred']/datos_inverter['Vred'],2)  
                else:
                    datos_inverter['Ired'] = 0
                    
                datos_inverter['Vred'] = round(datos_inverter['Vred'],2)
                datos_inverter['Iplaca'] = round(datos_meter['Wplaca']/datos_inverter['Vred'],2)
                datos_inverter['Fred'] = round(datos_inverter['Fred'],2)
                     
            datos= datos_inverter
            
            tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
            """
            tiempo_sg = time.time()
            
            datos['Tiempo'] = tiempo
            datos['Tiempo_sg'] = tiempo_sg
            
            print('datos=',datos)
            """
            
            if datos != None :
                try:####  ARCHIVOS RAM en BD ############ 
                    salida = json.dumps(datos)
                    
                    if DEBUG:
                        print()
                        print (f'id_equipo = {equipo}{N_equipo} -- salida=',salida)
                        print()
                    
                    sql = (f"UPDATE equipos SET `tiempo` = '{tiempo}',sensores = '{salida}' WHERE id_equipo = '{equipo}{N_equipo}'") # grabacion en BD RAM
                    cursor.execute(sql)
                    db.commit()
                except:
                    print(Fore.RED+f'error, Grabacion tabla RAM equipos en {equipo}{N_equipo}')
                 
            
            time.sleep(max (t_muestra_fronius[indice]-(time.time()-t1),0))
            
        except KeyboardInterrupt:   # Se ha pulsado CTRL+C!!
            break
        except:
            print(f"error no conocido en lectura {equipo}{indice}")
            time.sleep(5)
            #sys.exit()

    

if __name__ == '__main__':
    
    usar_equipo = usar_fronius #
    equipo = 'FRONIUS'
    
    equipos_activos = [ i for i in range(len(usar_equipo)) if usar_equipo[i] == 1 ] # indices equipos activos

    print (Fore.RESET+'=' * 50)
    print(Fore.BLUE+'equipos_activos=')
    
    for i in equipos_activos: 
        print(Fore.RED+f' IP= {IP_FRONIUS[i]} - {Fore.BLUE} usar_meter= {usar_meter_fronius[i]} - tmuestra= {t_muestra_fronius[i]}')
        print()
        
        # Comprobacion BD
        try:
            db = MySQLdb.connect(host = servidor, user = usuario, passwd = clave, db = basedatos)
            cursor = db.cursor()
            
            if i == 0: N_equipo = ""
            else: N_equipo = f"{i}"
            
            Sql = f""" CREATE TABLE IF NOT EXISTS `fronius` (
               `id` int(11) NOT NULL AUTO_INCREMENT,
               `Tiempo` datetime NOT NULL,
               `xxxx` float NOT NULL DEFAULT 0,
               `yyyy` float NOT NULL DEFAULT 0,
               PRIMARY KEY (`id`),
               KEY `Tiempo` (`Tiempo`)
               ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci
               """                
            
            """ # no se crea tabla especifica
            import warnings # quitamos el warning que da si existe la tabla equipos
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                cursor.execute(Sql)   
            db.commit()
            """
            
            try: # creacion registro en tabla equipos
                cursor.execute("""INSERT INTO equipos (id_equipo,sensores) VALUES (%s,%s)""",
                          (f'{equipo}'+N_equipo,'{}'))   
                db.commit()
            except:
                pass     
            
            cursor.close()
            db.close()
        
        except:
            print (Fore.RED+ 'ERROR inicializando BD RAM')
            sys.exit()
        
        # Arrancando proceso
        multiprocessing.Process(target = equipo_lectura,args=(i,),name = f'{equipo}{i}').start()
    
    time.sleep(5)   
    print (Fore.RESET+'=' * 50)
    
    Procesos= multiprocessing.active_children() # lista procesos activos
    print ('Procesos activos=',Procesos)
    
    # Bucle     
    while True:
        if DEBUG: print ('Bucle Main')
        time.sleep(10)
    
    sys.exit()
    
    
    
