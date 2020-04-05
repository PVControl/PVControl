#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys, subprocess
import logging, traceback
from csvFv import CsvFv
from Bd import *
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from Parametros_FV import *

if usar_srne == 0:
    #print (commands.getoutput('sudo systemctl stop srne'))
    print (subprocess.getoutput('sudo systemctl stop srne'))
    sys.exit()

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

    archivoFv = '/run/shm/datos_srne.csv' # archivo ram FV
    archivoTemp = '/run/shm/datos_temp.csv' # archivo ram temperatura

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
        self.csvfv = CsvFv(self.archivoFv)
        self.csvtemp = CsvFv(self.archivoTemp)

    ##
    # convierte el estado del regulador
    # @param codigo (byte)
    # @return (string) estado del regulador
    def getEstado (self, codigo):
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


    def getDatosFV(self):
        self.csvfv = CsvFv (self.archivoFv)
        return self.csvfv.leerCsv()

    def getDatosTemp(self):
        self.csvtemp = CsvFv (self.archivoTemp)
        return self.csvtemp.leerCsv()


    ##
    # Guardar datos en archivo ram y base de datos
    def guardarDatosFV (self):
        # escribir archivo ram
        self.csvfv.escribirCsv(self.datos)

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
            Res = self.modbus.read_holding_registers(0x0101, 9, unit=1)
            # recoger 1 registro (0x0120)
            R_Est = self.modbus.read_holding_registers(0x0120, 2, unit=1)

            if not Res.isError() and not R_Est.isError():
                r = Res.registers[0:]
                if len(r)==9:

                    # Procesado de los datos FV ########
                    Vbat = float(r[0]/10)
                    Iplaca = float(r[1]/100)
                    Vplaca = float(r[6]/10)
                    Ipanel = float(r[7]/100)
                    Wplaca = int(r[8])
                    x = format(r[2], '04x')
                    Treg = int(x[:2],16)
                    Tbat = int(x[2:],16)

                    est = R_Est.registers[0]
                    estInt = int(format(est, '02x')) # 8 lower bits
                    Estado = self.getEstado(estInt)

                    self.datos = {'Tiempo_sg':tiempo_sg, 'Tiempo':tiempo,
                                    'Vbat':Vbat, 'Vplaca':Vplaca, 'Iplaca':Iplaca,
                                    'Estado':Estado}
                    #print(self.datos)
                    #print(Vbat,Iplaca,Vplaca,Ipanel,Wplaca,Estado,Tbat,Treg)
                    self.guardarDatosFV()
                    logging.info ("Datos: %s %s %s %s", str(Vbat), str(Vplaca), str(Iplaca), Estado)

                    # Procesado de los datos de temperatura ########
                    if tipo_sensortemperatura == "SRNE":
                        self.datos = {'Tiempo_sg': tiempo_sg,'Tiempo': tiempo,
                                        'Temp0':Tbat,'Temp1':Treg,'Temp2':0,
                                        'Temp3':0,'Temp4':0,'Temp5':0}
                        self.csvtemp.escribirCsv(self.datos)
                        logging.info (__class__.__name__ + ": Tbat="+str(Tbat)+"|Treg="+str(Treg))
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
    #main(sys.argv[1:])
    logging.basicConfig(level=DEBUG_LEVEL)
    Srne(dev_srne).leerRegistros()




