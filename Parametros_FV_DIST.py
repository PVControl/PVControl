# ------------------------------------------------------------------
######    PARAMETROS INSTALACION PVControl+  -- version: 2022-09-22
# ------------------------------------------------------------------

# ====================================================================
# ====================================================================
#             1.- SECCION PRINCIPAL PARAMETRIZACION        
# ====================================================================
# ====================================================================


########################
###### Simulacion ######
########################
simular = 0         # Simulacion datos FV --- 1 para simular....0 para no simular
simular_reles = 0   # Simular reles fisicos
# -----------------------------------------------

################################
##### Parametros sensores ######
################################

# 'Variable' : {'Equipo':"expresion captura",'Max':Valor maximo, 'Min':Valor minimo,......},

## Se pueden crear las variables que se quieran y con el nombre que se quiera
## La "expresion de captura" puede ser cualquier expresion python3 valida
## En los programas de captura que utilicen la tabla en BD RAM la sintaxis sera.... "d_['CLAVE']['Variable']".... d_['ADS1']['Vbat'], d_['HIBRIDO']['Vbat'],...
## En los programas de captura que aun utilicen los archivos pkl la sintaxis sera.... "d_clave['Variable']".... d_sma['Vbat'], d_srne['Vbat'],...
## Si se definen las claves 'Max' y 'Min' se enviara un log si la captura esta fuera de dichos margenes 
 
sensores ={
'Vbat'    : {'Equipo':"d_['HIBRIDO']['Vbat']", 'Max':66, 'Min':11},     # Sensor de Voltaje bateria
'Vplaca'  : {'Equipo':"d_['HIBRIDO']['Vplaca']", 'Max':500, 'Min':-5},  # Sensor de Voltaje placa

'Ibat'    : {'Equipo':"d_['HIBRIDO']['Ibat']", 'Max':200, 'Min':-200}, # Sensor de Intensidad bateria
'Iplaca'  : {'Equipo':"d_['HIBRIDO']['Iplaca']", 'Max':200, 'Min':-1}, # Sensor de Intensidad Placas

'Aux1'  : {},    # Sensor Aux1
'Aux2'  : {},    # Sensor Aux2
'Aux3'  : {},    # Sensor Aux3
'Aux4'  : {},    # Sensor Aux4
'Aux5'  : {},    # Sensor Aux5
'Aux6'  : {},    # Sensor Aux6
'Aux7'  : {},    # Sensor Aux7

'Vred' : {},   # Sensor Voltaje de red 
'Ired' : {},   # Sensor Intensidad de red
'EFF'  : {},   # Eficienca Conversion 

'Temp_Bat': {},  #  Sensor Temperatura

# Expresiones calculadas
'Wbat' : {'Equipo': "Ibat * Vbat"}, #  Potencia de/a baterias
'Wplaca' : {'Equipo': "d_['HIBRIDO']['Wplaca']"}, #  Potencia de placas
'Wred' : {'Equipo': "Ired * Vred"},     #  Potencia de/a red
'Wconsumo': {'Equipo': "d_['HIBRIDO']['PACW']"}, # Consumo

'Temp': {'Equipo':"Temp_Bat"},  #  Temperatura que se guarda en BD y muestra en reloj Web


'Grafica_Aux'  : {"[0,1,Vbat,Iplaca,Ibat]"},  # [Activar, Nmuestras, lista variables....]

}

# -----------------------------------------------

######################################
###### Parametros Base de Datos ######
######################################
servidor = "localhost"
usuario = "rpi"
clave = "fv"
basedatos = "control_solar"

grabar_datos_s = "False"   # expresion para grabar cada muestra en la tabla datos_s
                           # Ejemplos: 'True'.. 'False'.. 'Vplaca > 10'... 'PWM > 0'

t_muestra_max = 6     # valor para grabar en el log si tarda mas el bucle en ejecutarse
# -----------------------------------------------

##################
###### MQTT ######
##################
mqtt_broker  = "localhost"
mqtt_puerto  = 1883
mqtt_usuario = "rpi"
mqtt_clave   = "fv"


##### Subcripciones #####
usar_mqtt_suscripciones = 0  # activa servicio fv_mqtt.py que se suscribe a los topics que se especifiquen en mqtt_suscripciones  
               # guarda lo capturado en la tabla ram 'equipos' ... diccionario=d_['MQTT'] / servicio = fv_mqtt                

mqtt_suscripciones=[] #  lista de topics a los que se suscribe fv_mqtt.py para guardar en tabla equipos.. diccionario=d_['MQTT']


##### Publicaciones #####
usar_mqtt_publicaciones =  0    # 1 = Publica por MQTT los topic definidos en mqtt_publicaciones...... 0= No publica por MQTT  
mqtt_topic_raiz = "PVControl/"  # Raiz del topic a publicar

#  Tuplas [Nombre Topic, Variable, frecuencia en sg (0 deshabilita, por defecto = Tmuestra * Nmuestra)]
mqtt_publicaciones = [["Wplaca","Wplaca"],
                      ["Vbat","Vbat"],
                      ["Ibat","Ibat",10],
                      ["SOC","SOC",15],
                      ["DatosFV","d_['FV']",0]] # publica diccionario d_[FV] en topic PVControl/DatosFV para poder ser usado por Home Assistant

# -----------------------------------------------

# ====================================================================
# ====================================================================
#    2.- SECCION PARAMETRIZACION SEGUN EQUIPAMIENTO INSTALADO        
# ====================================================================
# ====================================================================


################################
###### Parametros Bateria ######
################################
AH = 100.           # Capacidad en Ah de la Bateria a C20 (poner 0 para instalaciones sin Bateria)
CP = 1.              # Indice Peukert
EC = 1.              # Eficiencia Carga
vsis = 4.            # Voltaje sistema - 1=12V  2=24V   4=48V
vflotacion = 13.7   # Valor por defecto de flotacion a 25??C a 12V (no se usa por ahora)
# -----------------------------------------------

#######################################################
###### Parametros ADS1115  - Permite hasta 4 ADS ######
#######################################################
usar_ADS = [0,0] # activar o no el ADS
nombre_ADS = ['ADS1','ADS4']                                         # Nombre de los ADS
direccion_ADS = [72,75]                                              # direccion I2C del ADS

var_ADS = [['Vbat','Aux1', 'Vplaca','Aux2'],['Ibat','','Iplaca','']] # Nombre de las variables a capturar

tmuestra_ADS = [1,1]                                                 # tiempo en sg entre capturas
rate_ADS = [[250,250,250,250],[250,0,250,0]]                     # datarate de lectura
bucles_ADS = [[10,5,5,5], [5,0,5,0]]                                 # Numero de bucles de lectura

gain_ADS = [[2,2,2,2], [16,0,16,0]]                                # Voltios Fondo escala 1=4,096V - 2=2.048V - 16= 256mV
modo_ADS = [[1,1,1,1], [3,0,3,0]]                                    # 0=desactivado, 1=disparado, 2= Continuo, 3=diferencial, 4=diferencial_continuo
res_ADS = [[47.46,47.46,47.46,47.46],[100/0.075,0,100/0.075,0]]      # ratio lectura ADS - Lectura real

# -----------------------------------------------
#########################
###### Multiplexor ######
#########################
usar_mux = 0   # Poner el numero de celdas a monitorizar (0= desactivar)...diccionario = d_['MUX'] / servicio = fv_mux

t_muestra_mux = 5 # segundos entre capturas del mux
n_muestras_mux = 4        # grabar en BD en tabla permanente cada X capturas 

pin_ADS_mux1 = "A2_2" #A2_1 = entrada A2 del ADS1, #A2_2 = entrada A2 del ADS2
                      #A2_3 = entrada A2 del ADS3, #A2_4 = entrada A2 del ADS4
                      
pin_ADS_mux2 = 'A3_2' #A3_1 = entrada A3 del ADS1, #A3_2 = entrada A3 del ADS2
                      #A3_3 = entrada A3 del ADS3, #A3_4 = entrada A3 del ADS4

captura_mux = "S"  # D = lectura modo diferencial.... S = modo simple
                   # ATENCION si el modo de captura es diferencial se deben usar los 2 MUX y 
                   #   configurar en la PCB las salidas del MUX para usar las entradas A2 y A3 del mismo ADS
             
gain_mux = 1       # Voltios Fondo escala del ADS1115... 1=4,096 - 2=2.048

r_mux = [47] * 32  # Ratio Divisores de Voltaje de cada entrada de los Mux - Ejecutar el programa.. python3 fv_mux_calibracion.py  ... para calibrar los valores medidos
                   # Dicho programa creara en la BD la tabla "parametros1" y un registro donde se incluira la calibracion realizada

celdas_log_dif = 0.5 # diferencia entre la celda mas alta y la mas baja para mandar log

# -----------------------------------------------
#################################################
###### HIBRIDO  -  Permite hasta 9 Equipos ######
#################################################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Vbat, Vplaca,...)  usa el Hibrido o se quiere guardar en BD en la tabla 'Hibrido'
## se debe poner usar hibrido = 1

usar_hibrido = [0] #1 para leer datos Hibrido ..... 0 para no usar

dev_hibrido = ["/dev/hidraw0"]  # puerto donde reconoce la RPi al Hibrido
usar_crc = [1]                  # 1 para comandos del hibrido con CRC... 0 para no a??adir CRC

t_muestra_hibrido = [5]         # Tiempo en segundos entre muestras del Hibrido
publicar_hibrido_mqtt = [1]     # Publica o no por MQTT los datos capturados del Hibrido

grabar_datos_hibrido = [1]      # 1 = Graba la tabla Hibrido... 0 = No graba
n_muestras_hibrido = [1]        # grabar en BD en tabla 'hibrido' cada X capturas del Hibrido 

protocolo_hibrido = [30]        # N?? de Protocolo del Hibrido (30 o 18)

# -----------------------------------------------

#########################
###### DALY ######
#########################
usar_daly = 0                   # 1 = Se usa 0 = No se usa
t_muestra_daly = 1              # segundos entre capturas para tabla en RAM 
grabar_datos_daly = 1           # 1 = Graba la tabla ... 0 = No graba
leer_soc_daly = 1               # 1 = leer soc ibat vbat .... 0 = NO SE USA
leer_temp_daly = 0              # 1 = leer la temperaturas ... 0 = NO SE USA 
leer_ciclos_daly = 1            # 1 = leer los ciclos el numero de celdas y varias cosas mas que no tengo claro = 0 NO SE USA
leer_V_Max_Min_daly = 1         # 1 = leer el valor max y min de las celdas ... 0 = NO SE USA
n_muestras_daly = 5             # grabar en BD en tabla permanente cada X capturas 
Valor_error_max_daly = 4.5      # no grabar si alguna lectura da este valor
Valor_error_min_daly = 2.8      # no grabar si alguna lectura da este valor
dev_daly = "/dev/ttyUSB0"       # puerto donde reconoce la RPi al Hibrido


# -----------------------------------------------

#####################
###### VICTRON ######
#####################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa el Victron o se quiere guardar en BD en la tabla 'victron'
## se debe poner usar victron = 1

usar_victron = 0              # 1 para leer datos victron ..... 0 para no usar

dev_victron = "/dev/ttyUSB0"  # puerto donde reconoce la RPi al Victron

grabar_datos_victron = 0      # 1 = Graba la tabla victron... 0 = No graba
t_muestra_victron = 5         # Tiempo en segundos entre muestras

iplaca_victron_max = 99
iplaca_victron_min = 0

# -----------------------------------------------
#####################
###### MUST ######
#####################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa el MUST o se quiere guardar en BD en la tabla 'must'
## se debe poner usar must= 1

usar_must = 0              # 1 para leer datos victron ..... 0 para no usar
n_equipos_must = 0         #n??mero de inversores en paralelo. Si s??lo hay uno, marcar 1.
dev_must = "/dev/ttyUSB0"  # puerto donde reconoce la RPi al Must

grabar_datos_must= 0      # 1 = Graba la tabla Must... 0 = No graba
t_muestra_must = 1         # Tiempo en segundos entre muestras + numero de equipos

iplaca_must_max = 99
iplaca_must_min = 0

# -----------------------------------------------
#################
###### BMV ######
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa el BMV o se quiere guardar en BD en la tabla 'bmv'
## se debe poner usar bmv = 1

usar_bmv = 0              # 1 para leer datos victron ..... 0 para no usar

dev_bmv = "/dev/serial0"  # puerto donde reconoce la RPi al BMV

grabar_datos_bmv = 0      # 1 = Graba la tabla bmv... 0 = No graba
n_muestra_bmv = 5         # # Numero de muestras para guardar en BD tabla bmv

# -----------------------------------------------
#################
###### SMA ######
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa el SMA o se quiere guardar en BD en la tabla 'sma'
## se debe poner usar sma = 1

usar_si = 0               # 1 para leer datos del SI ..... 0 para no usar
usar_sb1 = 0              # 1 para leer datos del SB1 ..... 0 para no usar
usar_sb2 = 0              # 1 para leer datos del SB2 ..... 0 para no usar
usar_smameter = 0        # 1 para leer datos del meter SMA ..... 0 para no usar
IP_SI = "192.168.0.24"    # IP del SI
IP_SB1 = "192.168.0.253"  # IP del SB1
IP_SB2 = "192.168.0.252"  # IP del SB2

# -----------------------------------------------
#################
#### FRONIUS ####
#################

## Se admiten varios equipos fronius... incluir separado por comas los distintos parametros....
## por ejemplo para 2 equipos....
##    usar_fronius = [1,1]....IP_FRONIUS = ["192.168.1.101","192.168.1.102"] ...etc
 
## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa fronius se debe poner usar fronius = [1]

usar_fronius = [0]          	 # 1 para leer datos del fronius..... 0 para no usar
usar_meter_fronius = [0]         # 1 para activar lectura de contador de Fronius
IP_FRONIUS = ["192.168.0.24"]    # IP del FRONIUS
t_muestra_fronius = [5]          # Tiempo en segundos entre capturas 
# -----------------------------------------------
#################
####  HUAWEI ####
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa fronius se debe poner usar huawei = 1

usar_huawei = 0                # 1 para leer datos del huawei..... 0 para no usar
IP_HUAWEI = "192.168.0.24"    # IP del huawei
t_muestra_huawei = 5          # Tiempo entre capturas
# -----------------------------------------------
#################
####  GOODWE ####
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa fronius se debe poner usar goodwe = 1

usar_goodwe = 0                 # 1 para leer datos del goodwe..... 0 para no usar
IP_GOODWE = "192.168.0.100"     # IP del goodwe
t_muestra_goodwe = 5
usar_batgoodwe = 0              # 1 para usar bater??a y 0 para no usar

# -----------------------------------------------
##################
###### SRNE ######
##################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa el SRNE o se quiere guardar en BD en la tabla 'srne'
## se debe poner usar srne = 1

usar_srne = 0              #1 para leer datos srne ..... 0 para no usar
    
dev_srne = "/dev/ttyUSB0"  # /dev/ttyUSB0" # USB  -  "/dev/ttyS0" # TTL

grabar_datos_srne = 1      # 1 = Graba la tabla srne... 0 = No graba

iplaca_srne_max = 85
iplaca_srne_min = 0

#####################
###### SDM120C ######
#####################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor usa sdm120c se debe poner usar_sdm120c = 1

usar_sdm120c = [0] 
dev_sdm120c = ["/dev/ttyUSB0"]  # puerto donde reconoce la RPi al equipo
t_muestra_sdm120c = [5]         # Tiempo en segundos entre muestras
publicar_sdm120c_mqtt = [0]     # Publica o no por MQTT los datos capturados (no implementado aun)
grabar_datos_sdm120c = [1]      # 1 = Graba la tabla Hibrido... 0 = No graba
n_muestras_sdm120c = [1]        # grabar en BD cada nmuestras

# -----------------------------------------------
##################
###### EASTRON ######
##################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor usa el eastron se debe poner usar eastron = 1

usar_eastron = 0       # 1 para leer datos ..... 0 para no usar
dev_eastron = ""       # /dev/ttyUSB0" # USB  

# -----------------------------------------------
######################################
###### DEYE, TURBO ENERGY,...   ######
######################################

usar_deye = [0] 
dev_deye = ["/dev/ttyUSB0"]  # puerto donde reconoce la RPi al equipo
t_muestra_deye = [1]         # Tiempo en segundos entre muestras
con_bateria_deye = [0]       # Inversor con bateria = 1 , sin bateria = 0

grabar_datos_deye = [0]      # 1 = Graba la tabla deye.. 0 = No graba .... NO IMPLEMENTADO AUN
n_muestras_deye = [5]        # grabar en BD cada nmuestras .... NO IMPLEMENTADO AUN

usar_telegram_deye = [1]          # Manda un mensaje por Telegram cuando cambia de estado el equipo


# -----------------------------------------------
##################
### BROADLINK ####
##################

## Indicar si se tiene instalado alg??n equipo de broadlink para uso AA


array_IP = ['192.168.1.234','192.168.1.235']  # Indicar IP??s de equipos Broadlnk
array_reles = [271,281]     #Indicar rel??s en el mismo orden que las IPs anteriores a asignar a los rel??s.

###########################
###### Pantalla OLED ######
###########################
OLED_salida1 =[0,1,2,3] # secuencia de pantallazos modelo 1, 2, 3 o 4...0=Logo
OLED_salida2 =[4] # secuencia de pantallazos modelo 1, 2, 3 o 4...0=Logo

# -----------------------------------------------
# ====================================================================
# ====================================================================
#    3.- SECCION PARAMETRIZACION SERVICIOS ADICIONALES 
# ====================================================================
# ====================================================================

###############################
###### Telegram & MOTION ######
###############################
usar_telegram = 0 # 1 para usar  ..... 0 para no usar
TOKEN ='XXXXXX:YYYYYYYYYY......'# bot Telegram...cambiar por el que cada uno de de alta

# ID de Usuarios autorizados a mandar mensajes, los msg periodicos se mandan al primer declarado
Aut = [111111,22222] # Lista de ID de Telegram autorizados

cid_alarma = 1111111 # # Id Telegram a donde se enviara la foto/video de alarma

msg_periodico_telegram = 0 # 1 = Manda un mensaje resumen por Telegram cada Hora -- 0 = No manda mensaje

# Configuracion mensaje Telegram

#  --- IMAGEN ---
region_captura_pantalla = (0, 0, 0, 0, 0) #(Activar envio imagen, X, Y, Ancho, Alto) manda la captura de la region de pantalla

#  --- TEXTO ----
#   Se puede incluir...  {cualquier campo de la tabla equipos}, texto, unicodes,....
#   Tambien existen algunas variables propias definidas 
#      {L_celdas}         Linea con valor max y min de las celdas
#      {L_reles}          Una unica linea con informacion resumida de los reles
#      {L_reles_unicode}  Una linea por cada rele
#      {L_temp}           Una linea con temperaturas CPU y DS18b20 
#      {temperaturas}     Una linea con temperaturas DS18b20 
#      {L_ip_local}       IP LAN local
#      {L_ip}             IP WAN

#unicodes para categorizar reles  ....primera dupla= ('texto que no exista en reles', 'unicode por defecto')
unicode_reles_telegram = [('??????###','\U0001F6A6'),('luz','\U0001F526'),('cale','\U0001F525')] # duplas (texto, unicode) para primer simbolo de {L_reles_unicode}

msg_telegram = ["\U0001F50B <b><u>Bater??a</u></b>: (<code>{d_['FV']['Mod_bat']}</code>)",
				"     SOC: <b>{d_['FV']['SOC']:.1f}</b>%     \U000024CB <b>{d_['FV']['Vbat']:.1f}</b>V     \U000024BE <b>{d_['FV']['Ibat']:.1f}</b>A",
				#"     \U0001F4CA {L_celdas}",

                "\U0001F31E <b><u>Placas</u></b>:",
                "     \U000024C5 <b>{d_['FV']['Wplaca']:.0f}</b>W     \U000024BE <b>{d_['FV']['Iplaca']:.1f}</b>A     \U000024CB <b>{d_['FV']['Vplaca']:.0f}</b>V",

                "\U0001F4A1 <b><u>Consumo</u></b>:",
                "     \U000024C5 <b>{d_['FV']['Wconsumo']:.0f}</b>W     \U000024BE <b>{d_['FV']['Iplaca']-d_['FV']['Ibat']:.1f}</b>A     PWM: <b>{d_['FV']['PWM']:.0f}</b>",
                
                "\U00002753 <b><u>Rel??s</u></b>:",
                "<b>{L_reles_unicode}</b>",
                
                #"\U0001F50C <b><u>Red</u></b>:",
                #"     \U000024C5 <b>{d_['FV']['Wred']:.0f}</b>W     \U000024BE <b>{d_['FV']['Ired']:.1f}</b>A     \U000024CB <b>{d_['FV']['Vred']:.0f}</b>V",

                "\U0001F4C6 <b><u>Diario (KWh)</u></b>:",
                "     \U0001F31E <b>{d_['FV']['Wh_placa']/1000:.1f}</b> \U0001F50B <i>{d_['FV']['Whp_bat']/1000:.1f}-{d_['FV']['Whn_bat']/1000:.1f}</i> = <b>{(d_['FV']['Whp_bat']-d_['FV']['Whn_bat'])/1000:.1f}</b> \U0001F4A1 <b>{(d_['FV']['Wh_consumo'])/1000:.1f}</b>",
                #"     \U0001F50C <b>{(d_['FV']['Wh_red'])/1000:.1f}</b>",

                "\U0001F321 <b><u>Temperaturas (??C)</u></b>:",
                "     Bat: <b>{d_['FV']['Temp']}</b> / CPU: <b>{d_['TEMP']['Temp_cpu']:.1f}</b>",

                "\U0001F4BB <b><u>Conexi??n (IP)</u></b>:",
                "     \U0001F3E0 {L_ip_local}  \U0001F30D <span class='tg-spoiler'>{L_ip}</span>",
                ]

# -----------------------------------------------

#########################
###### PV_OUTPUT ########
#########################
usar_pvoutput = 0 # 1 para usar  ..... 0 para no usar

pvoutput_key = "xxxxxxxx" # Key PVoutput
pvoutput_id = "1233455"
# -----------------------------------------------

#########################################################
###### Vigilancia por Camara con Motion y Clarifai ######
#########################################################

usar_motioneye = 0 # activa servicio motioneye

motion_telegram = 0 # 1 = Envia foto deteccion a Telegram

motion_clarifai = 0 # activa reconocimiento por Clarifai
api_key = 'xxxxxxxxxxxx' # Key Clarifai
workflow_id = 'yyyyyyyy' # Nombre del Workflow creado en Clarifai

# fconfiguraci??n horaria para motion
# dias de la semana 1-7. Horas 24 bits 0=no grabar 1=si
horario_alarma = {
    1:'111111110000000000000000',
    2:'111111110000000000000000',
    3:'111111110000000000000000',
    4:'111111110000000000000000',
    5:'111111110000000000000000',
    6:'111111111000000000000000',
    7:'111111111000000000000000'}

# -----------------------------------------------



