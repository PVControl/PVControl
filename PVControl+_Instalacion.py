#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Versión 2022-05-01


# Programa de Instalacion del PVControl+
#
# Ejecutar desde /home/pi con el siguiente comando

#    sudo python3 PVControl+_Intalacion.py opciones

#       opciones posibles:  
#          -c  implica clonar repositorio git
#          -d  instala docker y Home Assistant   
#          -m  instala motionEye   


# Si ya esta clonado el repositario git y solo se quiere reinstalar....
#    sudo python3 PVControl+_Intalacion.py


import os
import time
import subprocess #,commands
import sys
import colorama # colores en ventana Terminal
from colorama import Fore, Back, Style
colorama.init()
import click

time.sleep(1)
#'apt autoremove','apt remove apache2','apt purge apache2',
#'apt remove php*','apt purge php*',
#'apt remove mariadb*','apt purge mariadb*'



lista1 = [#clonacion PVControl+
         'git clone https://git.code.sf.net/p/pvcontrol/code PVControl+',
   
           ]


lista2 = [# Sistema, Apache & php
         'sudo apt update',
         'sudo apt install apache2 -y',
         'sudo apt-get full-upgrade',
         'curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg > /dev/null',
         'echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list',
         'sudo apt update',
         'sudo apt install php8.1 php8.1-cli php8.1-common php8.1-curl php8.1-gd php8.1-intl php8.1-mbstring php8.1-mysql php8.1-opcache php8.1-readline php8.1-xml php8.1-xsl php8.1-zip php8.1-bz2 libapache2-mod-php8.1 -y',
         
         
         # MariaDB
         'sudo apt install mariadb-server mariadb-client -y',
         'echo "CREATE USER \'rpi\'@\'localhost\' IDENTIFIED BY \'fv\';" | sudo mysql -uroot',
         'echo "GRANT ALL PRIVILEGES ON *.* TO \'rpi\'@\'localhost\' WITH GRANT OPTION;"  | sudo mysql -uroot',
         'echo "CREATE DATABASE control_solar;"  | sudo mysql -uroot',
         'sudo mysql -uroot control_solar < /home/pi/PVControl+/PVControl+.sql',
         'sudo mysql_secure_installation',
         'sudo apt install python3-mysqldb',
         
         # Phpmyadmin
         'wget https://www.phpmyadmin.net/downloads/phpMyAdmin-latest-all-languages.zip -O phpmyadmin.zip',
         'unzip phpmyadmin.zip',
         'rm phpmyadmin.zip',
         'sudo mv phpMyAdmin-*-all-languages /usr/share/phpmyadmin',
         'sudo chmod -R 0755 /usr/share/phpmyadmin',
         'sudo cp /home/pi/PVControl+/util/phpmyadmin.conf /etc/apache2/conf-available/phpmyadmin.conf',
         'sudo a2enconf phpmyadmin',
         'sudo systemctl reload apache2',
         'sudo mkdir /usr/share/phpmyadmin/tmp/',
         'sudo chown -R www-data:www-data /usr/share/phpmyadmin/tmp/',
         
         # WiringPi
         'cd /tmp',
         'wget https://project-downloads.drogon.net/wiringpi-latest.deb',
         'sudo dpkg -i wiringpi-latest.deb',
         'cd /home/pi',
         
         # Mosquitto MQTT
         'sudo apt-get install mosquitto mosquitto-clients -y' ,
         'sudo pip3 install paho-mqtt',
         'sudo bash -c \'echo "allow_anonymous false" > /etc/mosquitto/conf.d/default.conf\'',
         'sudo bash -c \'echo "listener 1883" >> /etc/mosquitto/conf.d/default.conf\'',
         'sudo bash -c \'echo "password_file /home/pi/PVControl+/passwd_mosquitto" >> /etc/mosquitto/conf.d/default.conf\'',       
         'sudo systemctl restart mosquitto',
         
         # Librerias Python3
         'sudo pip3 install adafruit-ads1x15',
         'sudo pip3 install pymodbus', 
         'sudo pip3 install pymodbusTCP',
         'sudo pip3 install minimalmodbus',
         'sudo pip3 install luma.core',
         'sudo pip3 install luma.oled',
         'sudo pip3 install esptool',
         'sudo pip3 install pyTelegramBotAPI',
         'sudo pip3 install timeout_decorator',
         'sudo pip3 install crc16',
         'sudo pip3 install clarifai',
         'sudo pip3 install clarifai-grpc',
         'sudo pip3 install goodwe',
         
         
         # Varios
         # motionEye
         #### ver .....https://github.com/motioneye-project/motioneye/wiki/Installation
         
         ]


lista3 = [# docker y HA
         
         # Docker
         'sudo apt install raspberrypi-kernel raspberrypi-kernel-headers',
         'curl -sSL https://get.docker.com | sh',
         'sudo usermod -aG docker pi',
   
         # Home Assistant
         'docker run -d --name homeassistant --privileged --restart=unless-stopped -e TZ=Europe/Madrid -v /home/pi/PVControl+/HA:/config --network=host  ghcr.io/home-assistant/home-assistant:stable',
           ]



lista4 = [# motionEye
         
          #### ver .....https://github.com/motioneye-project/motioneye/wiki/Installation
         
           ]


if '-c' in sys.argv:
    lista = lista1 + lista2
else:
    lista = lista2

if '-d' in sys.argv:
   lista += lista3
   
if '-m' in sys.argv:
   lista += lista4




for i in lista:
    print (Style.BRIGHT + Fore.YELLOW + '#' * 60)
    print (i)
    print ('#' * 60 + Fore.RESET)
    res = subprocess.run(i, shell=True)
    if res.returncode == 0:
        print (Style.BRIGHT + Fore.GREEN + '-' * 60)
        print('returncode:', res.returncode)
        print ('-' * 60)
    else:
        print (Style.BRIGHT + Fore.RED + '-' * 60)
        print('returncode:', res.returncode)
        print ('-' * 60)
        print ()
        salir = click.prompt(Fore.CYAN + '  Error detectado.... pulse una 0 para seguir o 1 para abortar ', type=str, default='0')
        if salir == '1': sys.exit()
        
    print(Fore.RESET)
    print()
    time.sleep(1)
    print(' ')
    
#Paginas web
print()
print(Fore.YELLOW+'######## Activando WEB PVControl+ #########')
res = subprocess.run(['sudo','rm', '-R','/var/www/html'])
res = subprocess.run(['sudo','ln', '-s','/home/pi/PVControl+/html','/var/www'])
print (Fore.GREEN+ '  ---- OK -----')
#Crontab
print()
print(Fore.YELLOW+'######## Activando Procesos CRONTAB #########')
res = subprocess.run(['sudo','cp', '-n', '/home/pi/PVControl+/etc/cron.d/pvcontrol.DIST','/home/pi/PVControl+/etc/cron.d/pvcontrol'])
res = subprocess.run(['sudo','chown', 'root','/home/pi/PVControl+/etc/cron.d/pvcontrol'])
res = subprocess.run(['sudo','ln', '-s','/home/pi/PVControl+/etc/cron.d/pvcontrol','/etc/cron.d/pvcontrol'], capture_output=True)
print (Fore.GREEN+ '  ---- OK -----')

#Escritorio
print()
print(Fore.YELLOW+'######## Enlaces en escritorio #########')
res = subprocess.run(['ln', '-s','/home/pi/PVControl+/PVControl_Configuracion_Inicial.py','/home/pi/Desktop/PVControl_Configuracion_Inicial.py'])
res = subprocess.run(['ln', '-s','/home/pi/PVControl+/Arrancar_servicios_PVControl+.py','/home/pi/Desktop/Arrancar_servicios_PVControl+.py'])
res = subprocess.run(['ln', '-s','/home/pi/PVControl+/Parar_Servicios_PVControl+.py','/home/pi/Desktop/Parar_Servicios_PVControl+.py'])
res = subprocess.run(['ln', '-s','/home/pi/PVControl+/Ver_Programas_en_Ejecucion_PVControl+.sh','/home/pi/Desktop/Ver_Programas_en_Ejecucion_PVControl+.sh'])
res = subprocess.run(['ln', '-s','/home/pi/PVControl+/PVControl+/PVControl_Instalacion_HomeAssistant.py','/home/pi/Desktop/PVControl_Instalacion_HomeAssistant.py'])

print (Fore.GREEN+ '  ---- OK -----')

print()
print(Fore.CYAN+'######## Proceso Completado #########')

