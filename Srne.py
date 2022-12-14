#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Versión 2020-05-04
import time
import sys, subprocess
import logging, traceback
from Bd import *
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json

from Parametros_FV import *


## Srne_Params.py ---------------------------------------------------
# Constantes de configuracion

# dev_srne= '/dev/ttyUSB0' # USB (configuracion en Parametro_FV.py)
#           '/dev/ttyS0' # TTL

# frecuencia de muestreo del regulador
FREQ_MUESTREO = 1 #seg
# frecuencia de grabación en la Bd
FREQ_BD = 5 #seg
# nivel de depuración (logging.CRITICAL, .ERROR, .WARNING, .INFO, .DEBUG)
DEBUG_LEVEL = logging.WARNING

#--------------------------------------------------------------------

##
# Gestion de reguladores modbus SRNE
# (Probado con el modelo MC-4885N25)
#
class Srne:

    ##
    # creacion e inicializacion del objeto
    def __init__(self, serialPort):
        logging.info(__class__.__name__ + ":Objeto creado")
        try:
            self.modbus = ModbusClient(method='rtu', port=serialPort, baudrate=9600, timeout=1)
            self.modbus.connect()
        except:
            logging.error(__class__.__name__ + ":Error de conexión Modbus")
            traceback.print_exc()
            return False
        self.datos = {}
        self.timeBd = time.time()
        self.bd = Bd()

    ##
    # convierte el estado del regulador
    # @param codigo (byte)
    # @return (string) estado del regulador
    def getEstadoSrne (self, codigo):
        if 0 > codigo > 6: return None
        else:
            estados = { 0 : "DEACTIVATED",
                        1 : "ACTIVATED",
                        2 : "BULK",
                        3 : "EQUALIZE",
                        4 : "ABSORTION",
                        5 : "FLOAT",
                        6 : "LIMITING"
                        }
            return estados[codigo]
            
    def getEstadoFv (self, codigo):
        if 0 > codigo > 6: return None
        else:
            estados = { 0 : "OFF",   # "DEACTIVATED"
                        1 : "BULK",  # "ACTIVATED",
                        2 : "BULK",  # "MPPT"
                        3 : "EQU",   # "EQUALIZE"
                        4 : "ABS",   # "ABSORTION"
                        5 : "FLOT",  # "FLOAT"
                        6 : "OFF",   # "LIMITING"
                        }
            return estados[codigo]

    ##
    # Guardar datos en archivo ram y base de datos
    def guardarDatosBd (self):
        # escribir en la bd si ha pasado eltiempo estipulado
        if time.time() - self.timeBd >= FREQ_BD:
            datosBd = self.datos
            del datosBd["Tiempo_sg"] # no guardamos este campo en la bd
            self.bd.insert("srne", self.datos)
            self.timeBd = time.time()

    ##
    # Lectura de registros por modbus y almacenamiento
    def leerRegistros(self):
        tiempo_sg = time.time()
        while True:
            if time.time()-tiempo_sg < FREQ_MUESTREO:
                time.sleep(0.1) # esperamos
                continue

            tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
            # recoger 9 registros (0x0101..0x0109)
            Res = self.modbus.read_holding_registers(0x0100, 10, unit=1)
            # recoger 1 registro (0x0120)
            R_Est = self.modbus.read_holding_registers(0x0120, 2, unit=1)

            if not Res.isError() and not R_Est.isError():
                r = Res.registers[0:]
                if len(r)==10:

                    # Procesado de los datos FV ########
                    s = format(r[0],'02x') # 8 lower bits
                    SoC = int(s,16)
                    Vbat = float(r[1]/10)
                    Iplaca = float(r[2]/100)
                    Vplaca = float(r[7]/10)
                    Ipanel = float(r[8]/100)
                    Wplaca = int(r[9])
                    x = format(r[3], '04x')
                    Treg = int(x[:2],16)
                    Tbat = int(x[2:],16)

                    est = R_Est.registers[0]
                    estInt = int(format(est, '02x')) # 8 lower bits
                    Estado = self.getEstadoFv(estInt)

                    self.datos = {'Tiempo_sg':tiempo_sg, 'Tiempo':tiempo,
                                    'Vbat':Vbat, 'Vplaca':Vplaca, 'Iplaca':Iplaca,
                                    'Estado':Estado,'SoC':SoC,
                                    'Temp0':Tbat,'Temp1':Treg}
                    datos_equipos = {'Vbat':Vbat, 'Vplaca':Vplaca, 'Iplaca':Iplaca,
                                    'Wplaca':Wplaca, 'Ipanel':Ipanel,
                                    'Estado':Estado,'SoC':SoC,
                                    'Temp0':Tbat,'Temp1':Treg}

                    # escribir tabla equipos en Bd
                    try:
                        salida = json.dumps(datos_equipos)
                        sql = (f"SELECT COUNT(*) FROM equipos WHERE id_equipo = 'SRNE'")
                        self.bd.cursor.execute(sql)
                        result = self.bd.cursor.fetchone()
                        if result[0]==0:
                            sql = (f"INSERT INTO equipos (id_equipo, tiempo, sensores) VALUES ('SRNE', '{tiempo}', '{salida}')")
                        else:
                            sql = (f"UPDATE equipos SET `tiempo` = '{tiempo}',sensores = '{salida}' WHERE id_equipo = 'SRNE'") # grabacion en BD RAM
                        self.bd.cursor.execute(sql)
                        #db.commit()
                    except:
                        print(f'error, Grabacion tabla RAM equipos en SRNE')
                    logging.info ("Datos: %s %s %s %s %s %s %s", str(Vbat), str(Vplaca), str(Iplaca),Estado, str(SoC), str(Tbat), str(Treg))
                    
                    # En la Bd guardamos los estados del protocolo SRNE
                    self.datos['Estado'] = self.getEstadoSrne(estInt)
                    self.guardarDatosBd()

                else:
                    self.modbus.close()
                    time.sleep(0.5)
                    self.modbus.connect()
                    logging.warning (__class__.__name__ + ':Error longitud registros SRNE')

            else:
                self.modbus.close()
                time.sleep(0.5)
                self.modbus.connect()
                logging.warning (__class__.__name__ + ':Error lectura registros SRNE')
            tiempo_sg = time.time()

        self.modbus.close()
        self.bd.desconecta()


if __name__ == '__main__':

    if usar_srne == 0:
        #print (commands.getoutput('sudo systemctl stop srne'))
        print (subprocess.getoutput('sudo systemctl stop srne'))
        sys.exit()

    #main(sys.argv[1:])
    logging.basicConfig(level=DEBUG_LEVEL)
    Srne(dev_srne).leerRegistros()





