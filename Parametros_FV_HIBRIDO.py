# ------------------------------------------------------------------
######    PARAMETROS INSTALACION PVControl+  -- version: 2020-11-21
# ------------------------------------------------------------------

################################
###### Parametros Bateria ######
################################
AH = 500.           # Capacidad en Ah de la Bateria a C20 (poner 0 para instalaciones sin Bateria)
CP = 1              # Indice Peukert
EC = 0.95           # Eficiencia Carga
vsis = 4            # Voltaje sistema - 1=12V  2=24V   4=48V
vflotacion = 13.7   # Valor por defecto de flotacion a 25ºC a 12V (no se usa por ahora)
# -----------------------------------------------

################################
##### Parametros sensores ######
################################

Vbat_sensor   = "d_hibrido['Vbat']"       # Sensor de Voltaje bateria ( ADS, d_hibrido['Vbat'], d_victron['Vbat'].....)
Vplaca_sensor = "d_hibrido['Vplaca']"     # Sensor de Voltaje placas ( ADS, d_hibrido['Vplaca'],d_victron['Vbat'].....)

Ibat_sensor   = "d_hibrido['Ibat']"       # Sensor de Intensidad Bateria ( ADS, d_hibrido['Ibat'], d_victron['Vbat'].....)
Iplaca_sensor = "d_hibrido['Iplaca']"     # Sensor de Intensidad Placas ( ADS, d_hibrido['Iplaca'], .....)

Aux1_sensor   = ""     # ADS, etc...
Aux2_sensor   = ""     # ADS, etc...

Wplaca_sensor  = "d_hibrido['Wplaca']"     # Iplaca * Vbat, d_hibrido['Wplaca'].....
Consumo_sensor = "Vbat * (Iplaca-Ibat)"    # Vbat * (Iplaca-Ibat), d_hibrido['PACW'].

Temperatura_sensor = ""                    #  d_ds18b20['Temp0'],d_ds18b20['Temp1'],..... d_snre['Temp0'].....

################################
###### Parametros ADS1115 ######
################################
SHUNT1 = 100.0/75        # Shunt Ibat (Amperios/mV)
SHUNT2 = 100.0/75        # Shunt Iplaca (Amperios/mV)

# Valor Voltaje divisor = Ventrada*R1/(R1+R2)
#Vbat
RES0 = (68+1.5)/1.5 * 12.63/12.33  # Divisor tension Vbat...(R2=68K..R1=1,5K) * ajuste por tolerancias en resistencias
RES0_gain = 2                   # Voltios Fondo escala 1=4,096 - 2=2.048
#Vaux
RES1 = (68+1.5)/1.5 #* 1.02735     # Divisor tension Aux1    
RES1_gain = 2                   # VoltiosFondo escala 1=4,096 - 2=2.048
#Vplaca
RES2 = (68+1.5)/1.5 #* 1.02618     # Divisor tension Vplaca
RES2_gain = 2                   # VoltiosFondo escala 1=4,096 - 2=2.048
#V...
RES3 = (68+1.5)/1.5 #* 1.02113     # Divisor tension Aux2
RES3_gain = 2                   # VoltiosFondo escala 1=4,096 - 2=2.048

# -----------------------------------------------

##########################################################
###### Parametros Mensaje error lectura incoherente ######
##########################################################
Vbat_max = 66     # Maximo voltaje bateria admisible para no dar aviso log
Vbat_min = 11     # Minimo voltaje bateria admisible para no dar aviso log

Aux1_max = 14
Aux1_min = -1

Aux2_max = 14
Aux2_min = -1

Vplaca_max = 500  # Maximo voltaje placas admisible para no dar aviso log
Vplaca_min = -5   # Minimo voltaje placas admisible para no dar aviso log

Ibat_max = 200    # Maxima intensidad bateria admisible para no dar aviso log
Ibat_min = -200   # Minima intensidad bateria admisible para no dar aviso log

Iplaca_max = 250
Iplaca_min = -1.5
Iplaca_error = 0.1 # poner el valor que por debajo se considerara Iplaca=0


Temp_max = 50       # Maxima temperatura admisible para no dar aviso log
Temp_min = -10      # Minima temperatura admisible para no dar aviso log

t_muestra_max = 6  # valor para grabar en el log si tarda mas el bucle en ejecutarse


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

# -----------------------------------------------
##################
###### MQTT ######
##################
mqtt_broker  = "localhost"
mqtt_puerto  = 1883
mqtt_usuario = "rpi"
mqtt_clave   = "fv"

pub_diver = 0 # publica datos ejecucion diver en "PVControl/Opcion/Diver"
pub_time  = 0  # publica datos de tiempo de ejecucion en "PVControl/Opcion/Time"
#mqtt_broker = 'iot.eclipse.org'


# -----------------------------------------------
###############################
###### Telegram & MOTION ######
###############################
usar_telegram = 0 # 1 para usar  ..... 0 para no usar
TOKEN ='XXXXXX:YYYYYYYYYY......'# bot Telegram...cambiar por el que cada uno de de alta

# ID de Usuarios autorizados a mandar mensajes, los msg periodicos se mandan al primer declarado
Aut = [111111,22222] # Lista de ID de Telegram autorizados

cid_alarma = 1111111 # # Id Telegram a donde se enviara la foto/video de alarma

msg_periodico_telegram = 0 # 1 = Manda un mensaje resumen por Telegram cada Hora -- 0 = No manda mensaje

#-------- Vigilancia por Camara con Motion y Clarifai
motion_telegram = 0 # 1 = Envia foto deteccion a Telegram
motion_clarifai = 0 # activa reconocimiento por Clarifai
api_key = 'xxxxxxxxxxxx' # Key Clarifai
workflow_id = 'yyyyyyyy' # Nombre del Workflow creado en Clarifai

# fconfiguración horaria para motion
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
#########################
###### PV_OUTPUT ########
#########################
usar_pvoutput = 0 # 1 para usar  ..... 0 para no usar

pvoutput_key = "xxxxxxxx" # Key PVoutput
pvoutput_id = "1233455"


# -----------------------------------------------
########################
###### Simulacion ######
########################
simular = 0  # Simulacion datos FV --- 1 para simular....0 para no simular
simular_reles = 0 # Simular reles fisicos
# -----------------------------------------------


# -----------------------------------------------
#########################
###### Multiplexor ######
#########################
usar_mux = 0   # Poner a 0 si no se utiliza un multiplexor de 16 canales de la PCB o el numero de canales a utilizar...maximo 16 por ahora

t_muestra_mux = 10 # segundos entre capturas del mux

pin_ADS_mux1 = "A2_2" #A2_1 = entrada A2 del ADS1
                      #A2_2 = entrada A2 del ADS2
                      #A2_3 = entrada A2 del ADS3
                      #A2_4 = entrada A2 del ADS4
                      
pin_ADS_mux2 = ''     #A3_1 = entrada A3 del ADS1
                      #A3_2 = entrada A3 del ADS2
                      #A3_3 = entrada A3 del ADS3
                      #A3_4 = entrada A3 del ADS4

R =(68+1.5)/1.5 * 12.94 / 12.72
r_mux1 =  [R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R] # Divisores de Voltaje de cada entrada del Mux1
r_mux2 =  [R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R] # Divisores de Voltaje de cada entrada del Mux2

celdas_log_dif = 0.1 # diferencia entre la celda mas alta y la mas baja para mandar log

# -----------------------------------------------
#####################
###### HIBRIDO ######
#####################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Vbat, Vplaca,...)  usa el Hibrido o se quiere guardar en BD en la tabla 'Hibrido'
## se debe poner usar hibrido = 1

usar_hibrido = 1 #1 para leer datos Hibrido ..... 0 para no usar

dev_hibrido = "/dev/hidraw0"  # puerto donde reconoce la RPi al Hibrido
usar_crc = 1                  # 1 para comandos del hibrido con CRC... 0 para no añadir CRC

t_muestra_hibrido = 5         # Tiempo en segundos entre muestras del Hibrido
publicar_hibrido_mqtt = 1     # Publica o no por MQTT los datos capturados del Hibrido

grabar_datos_hibrido = 1      # 1 = Graba la tabla Hibrido... 0 = No graba
n_muestras_hibrido = 5        # grabar en BD cada nmuestras

iplaca_hibrido_max = 80
iplaca_hibrido_min = 0


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
#################
###### BMV ######
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa el BMV o se quiere guardar en BD en la tabla 'bmv'
## se debe poner usar bmv = 1

usar_bmv = 0              # 1 para leer datos victron ..... 0 para no usar

dev_bmv = "/dev/serial0"  # puerto donde reconoce la RPi al BMV

grabar_datos_bmv = 0      # 1 = Graba la tabla bmv... 0 = No graba
t_muestra_bmv = 5         # Tiempo en segundos entre muestras

# -----------------------------------------------
#################
###### SMA ######
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa el SMA o se quiere guardar en BD en la tabla 'sma'
## se debe poner usar sma = 1

usar_sma = 0              # 1 para leer datos del sma ..... 0 para no usar
usar_si = 0               # 1 para leer datos del SI ..... 0 para no usar
usar_sb1 = 0              # 1 para leer datos del SB1 ..... 0 para no usar
usar_sb2 = 0              # 1 para leer datos del SB2 ..... 0 para no usar
IP_SI = "192.168.0.24"    # IP del SI
IP_SB1 = "192.168.0.253"  # IP del SB1
IP_SB2 = "192.168.0.252"  # IP del SB2

grabar_datos_sma = 0      # 1 = Graba la tabla sma... 0 = No graba

# -----------------------------------------------
#################
#### FRONIUS ####
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa fronius se debe poner usar fronius = 1

usar_fronius = 0          	# 1 para leer datos del fronius..... 0 para no usar
IP_FRONIUS = "192.168.0.24"    # IP del FRONIUS

# -----------------------------------------------
#################
####  HUAWEI ####
#################

## ATENCION ser congruente con lo que se ha puesto en el apartado de sensores
## Si algun sensor (Iplaca, Vplaca,...)  usa fronius se debe poner usar huawei = 1

usar_huawei = 0          	# 1 para leer datos del huawei..... 0 para no usar
IP_HUAWEI = "192.168.0.24"     # IP del huawei

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

# -----------------------------------------------
###########################
###### Pantalla OLED ######
###########################
OLED_salida1 =[0,1,2,3] # secuencia de pantallazos modelo 1, 2, 3 o 4...0=Logo
OLED_salida2 =[4] # secuencia de pantallazos modelo 1, 2, 3 o 4...0=Logo

# -----------------------------------------------

