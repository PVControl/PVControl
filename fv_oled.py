#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Versión 2022-01-14

import time,sys #, subprocess
import traceback
#import glob
import MySQLdb,json 

basepath = '/home/pi/PVControl+/'

print ('Arrancando_PVControl+- OLED')

#Parametros Instalacion FV
from Parametros_FV import *

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pathlib import Path

narg = len(sys.argv)
if str(sys.argv[narg-1]) == '-p1':
    DEBUG = 1
elif str(sys.argv[narg-1]) == '-p2':
    DEBUG = 2
elif str(sys.argv[narg-1]) == '-p3':
    DEBUG = 3
elif str(sys.argv[narg-1]) == '-p':
    DEBUG = 100
else:
    DEBUG = 0

if DEBUG !=0: print ('DEBUG=',DEBUG)

# Comprobacion numero de OLED instaladas
NUM_OLED = 0
try:
    serial = i2c(port=1, address=0x3C)
    disp1 = ssd1306(serial,rotate=0)

    
    NUM_OLED += 1
    #print('OLED 3C')
except:
    print(' No detectada OLED 3C')
    
    time.sleep(1)
    pass

if NUM_OLED == 1:
    try:
        serial = i2c(port=1, address=0x3D)
        disp2 = ssd1306(serial,rotate=0)
        NUM_OLED += 1
        print ('OLED 3C y 3D')
    except:
        print ('OLED 3C')
        pass
else:
    try:
        serial = i2c(port=1, address=0x3d)
        disp1 = ssd1306(serial,rotate=0)
        NUM_OLED += 1
        print ('OLED 3D')
    except:
        pass

if NUM_OLED == 0:
    #print (subprocess.getoutput('sudo systemctl stop fv_oled'))
    if DEBUG !=0: print ('NO detectada OLED - reintento en 1 minuto')
    sys.exit()

if NUM_OLED >= 1:
    
    image = Image.open(basepath+'pvcontrol_128_64.png').resize((disp1.width, disp1.height), Image.ANTIALIAS).convert('1')    
    disp1.display(image.convert(disp1.mode))   
    
    width = disp1.width
    height = disp1.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()
    font34 = ImageFont.truetype(basepath+'Minecraftia-Regular.ttf', 34)
    font16 = ImageFont.truetype(basepath+'Minecraftia-Regular.ttf', 16)
    font12 = ImageFont.truetype(basepath+'Minecraftia-Regular.ttf', 12)
    font10 = ImageFont.truetype(basepath+'Minecraftia-Regular.ttf', 10)
    font11 = ImageFont.truetype(basepath+'SmallTypeWriting.ttf', 15)
    font6 = ImageFont.truetype(basepath+'SmallTypeWriting.ttf', 10)

    OLED_contador1 = 0 # contador del pantallazo que presenta en secuencial
    OLED_salida_opcion1 = -1 # para elegir entre salida fija o secuencial
                            # se controla por MQTT con PVControl/Oled
                            # -1= secuencial....0,1,2,3... fija la pantalla marcada

if NUM_OLED == 2:
    #image = Image.open(basepath+'pvcontrol_128_64.png').resize((disp1.width, disp1.height), Image.ANTIALIAS).convert('1')    
    disp2.display(image.convert(disp2.mode))   

    OLED_contador2 = 0 # contador del pantallazo que presenta en secuencial
    OLED_salida_opcion2 = -1

#
def OLED(pantalla,modo):

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    if modo == 0:
        #image1 = Image.open('pvcontrol_128_64.png').resize((disp1.width, disp1.height), Image.ANTIALIAS).convert('1')
        image1 = Image.open(basepath+'pvcontrol_128_64.png').convert('1')
        if pantalla == 1:
            disp1.display(image1.convert(disp1.mode))   

        else:
            disp2.display(image1.convert(disp2.mode))   


    elif modo == 1:
        draw.rectangle((0, 0, 127, 20), outline=255, fill=0)
        draw.text((8, 0), 'SOC='+str(d_['FV']['SOC'])+'%', font=font16, fill=255)
        draw.rectangle((0, 20, 64, 46), outline=255, fill=0)
        draw.rectangle((64, 20, 127, 46), outline=255, fill=0)
        draw.text((4, 22),  'Vbat='+str(d_['FV']['Vbat']), font=font, fill=255)
        draw.text((69, 22), 'Ibat='+str(d_['FV']['Ibat']), font=font, fill=255)
        draw.text((4, 34),  'Vpla='+str(d_['FV']['Vplaca']), font=font, fill=255)
        draw.text((69, 34), 'Ipla='+str(d_['FV']['Iplaca']), font=font, fill=255)

        # Rele={2:'3X', 3:'XX0X', 7:'4'}
        L4 = 'R='
        Rele={}
        
        for r in d_['RELES']:
            tipo_rele = int(int(r)/100)
            if tipo_rele not in Rele.keys(): Rele[tipo_rele] = '' # inicializo valor
            valor = f"{d_['RELES'][r]['estado']/10:1.0f}"
            if valor == '10': valor = 'X'
            Rele[tipo_rele] += valor
        
        for r in Rele: L4 +=f'{r}{Rele[r]}-'
        L4 = L4[:-1] 
        
        draw.text((2, 49), L4, font=font11, fill=255)

    elif modo == 2:
        draw.rectangle((0, 0, 90, 31), outline=255, fill=0)
        draw.text((8, 1), 'Vbat='+str(d_['FV']['Vbat']), font=font11, fill=255)
        draw.text((8, 14), 'Ibat='+str(round(d_['FV']['Ibat'],0)), font=font11, fill=255)
        draw.rectangle((0, 31, 90, 63), outline=255, fill=0)     
        draw.text((8, 31), 'Vpla='+str(round(d_['FV']['Vplaca'],1)), font=font11, fill=255)
        draw.text((8, 45), 'Ipla='+str(round(d_['FV']['Iplaca'],0)), font=font11, fill=255)

        draw.rectangle((90, 0, 127, 20), outline=255, fill=255)     
        draw.text((100, 0), 'SOC', font=font, fill=0)
        draw.text((93, 10), str(d_['FV']['SOC']), font=font, fill=0)
        
        draw.rectangle((90, 22, 127, 42), outline=255, fill=255)     
        draw.text((95, 22), 'Temp', font=font, fill=0)
        draw.text((93, 32), str(d_['FV']['Temp']), font=font, fill=0)
        
        
        draw.rectangle((90, 44, 127, 63), outline=255, fill=255)     
        draw.text((95, 44), 'Exced.', font=font, fill=0)
        draw.text((100, 54), str(d_['FV']['PWM']), font=font, fill=0)

    elif modo==3:
        lineax=0
        lineay=0
        
        for r in d_['RELES']:
            valor = float(d_['RELES'][r]['estado'])
            if valor > 0:
                fill1=0
                fill2=255
            else:
                fill1=255
                fill2=0
            draw.rectangle((lineax, lineay, lineax+63, lineay+10), outline=255, fill=fill2)
            draw.text((lineax+2, lineay), d_['RELES'][r]['nombre'], font=font, fill=fill1)
            lineay +=10
            if lineay>53:
                lineax=66
                lineay=0
        
    elif modo == 4:
        if d_['FV']['SOC'] == 100:
            draw.rectangle((0, 0, 127, 63), outline=255, fill=255)
            draw.rectangle((3, 3, 124, 60), outline=255, fill=0)
            draw.rectangle((10, 10, 117, 53), outline=255, fill=255)
                        
            draw.text((13, 10), '100%', font=font34, fill=0)
        else:
            draw.rectangle((0, 0, 127, 63), outline=255, fill=0)
            draw.text((10, 10), str(d_['FV']['SOC'])+'%', font=font34, fill=255)
        
    if modo > 0:
        if pantalla == 1:  disp1.display(image.convert(disp1.mode))   
            
        if pantalla == 2:  disp2.display(image.convert(disp2.mode))   

 
 
#########################################################################################
# -------------------------------- BUCLE PRINCIPAL OLED --------------------------------------
#########################################################################################
try:
    
    time.sleep(10) # espera para que fv.py ponga en tabla equipos
    cp = 0
    while True:
        ee=10
        
        try:
            ## Capturando valores desde BD en tabla equipos
            ee=10.1
            db = MySQLdb.connect(host = servidor, user = usuario, passwd = clave, db = basedatos)
            cursor = db.cursor()
  
            sql = 'SELECT * FROM equipos' # WHERE id_equipo IN' ('FV','RELES')'# capturo todo...quizas lo logico solo FV y RELES
            nequipos = int(cursor.execute(sql))
           
            d_={}
            for row in cursor.fetchall(): d_[row[0]] = json.loads(row[2])
            if DEBUG == 100:
                print ('#'*40)
                print ('Equipos =',d_)
            cursor.close()
            db.close()
            
            ee=10.2    
            d_reles = d_['RELES']
            ee = 10.3
            nreles=len(d_['RELES'])
            ee = 10.4
            
            if DEBUG >= 1: 
                print('nreles=',nreles)
                print ('reles=',d_['RELES'])
                print('--------------------------------------------------')
            else:
                cp += 1
                print('x', end='',flush=True)
                if cp > 100: cp=0;print();print(time.strftime("%Y-%m-%d %H:%M:%S"),end='')
            
        except:
            print (f'error {ee} en lectura tabla equipos')
            time.sleep(0.3)
            break
            continue
            
      ## ------- Salida por pantalla OLED -------
        
        if NUM_OLED >= 1: #OLED numero 1
            if OLED_salida_opcion1 < 0: # <0 es salida secuencial
                OLED(1,OLED_salida1[OLED_contador1])
                OLED_contador1 += 1
                if OLED_contador1 >= len(OLED_salida1):
                    OLED_contador1=0
            else:
                 OLED(1,OLED_salida_opcion1)

        if NUM_OLED == 2: #OLED numero 2
            if OLED_salida_opcion2 < 0: # <0 es salida secuencial
                OLED(2,OLED_salida2[OLED_contador2])
                OLED_contador2 += 1
                if OLED_contador2 >= len(OLED_salida2):
                    OLED_contador2=0
            else:
                OLED(2,OLED_salida_opcion2)
        
        time.sleep(5)
        

except:
    print()
    print ('Error en bucle OLED',ee)
    traceback.print_exc()
finally:
    pass    








"""
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial,rotate=0)

with canvas(device, dither=True) as draw:
#with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "Hello World", fill="white")
    draw.text((40, 40), "Hello World", fill="white")
    
    draw.rectangle((10, 10, 30, 30), outline="white", fill="red")
"""
