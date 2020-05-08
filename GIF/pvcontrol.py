import tkinter as tk

from tkinter import *
from tkinter import ttk

import random,time,sys
import subprocess,shlex

sys.path.insert(1, '/home/pi/PVControl+/GIF')
sys.path.insert(1, '/home/pi/PVControl+')

from csvFv import CsvFv
import csv
import pickle,json

t_refresco=200 #ms
simular_datos = 0 # random datos FV

root = Tk()
root.geometry('700x600')
root.title('PVControl+  GUI')

canvas = Canvas(root, width = 400, height = 80,bg = 'seagreen')
canvas.pack(anchor = NW,fill = BOTH)#, expand = True)

foto_logo = PhotoImage(file = 'PVControl+.gif') #logo.gif

canvas.create_image(120, 40, image=foto_logo)
canvas.create_text(400, 30,text = 'TEST INSTALACION', font = ('Helvetica', 22, 'bold'), fill='DarkOrchid1')
canvas.create_text(400, 50, text = 'xxxx', font = ('Helvetica', 12, 'bold'), justify = 'center', fill='black')

canvas.update


style = ttk.Style(root)
# add label in the layout
style.layout('text.Horizontal.TProgressbar', 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': ''})],
                'sticky': 'nswe'}), 
              ('Horizontal.Progressbar.label', {'sticky': 'ns'})])
# set initial text
style.configure('text.Horizontal.TProgressbar', text='0 %')
# create progressbar
variable = tk.DoubleVar(root)


####### FRAME ARCHIVOS RAM #################################
f_csv = Frame(root,bg="darkkhaki",width=450,bd=2,height=100)
f_csv.pack(anchor= NW,)# fill = BOTH)#,expand = True)
f_csv.place(x=0,y=80)# fill = BOTH)#,expand = True)

d_fv_tit=Label(f_csv, relief ='groove',text=" datos_fv: ",font=("Verdana",7))
d_fv_tit.place(x=0, y=0, height=18,width = 100)
d_fv=Label(f_csv, relief ='ridge',fg="black",bg="lightyellow", font=("Verdana",7))
d_fv.place(x=100, y=0, height=18)
d_fv_txt = StringVar()

d_hibrido_tit=Label(f_csv, relief ='groove',text=" datos_hibrido: ",font=("Verdana",7))
d_hibrido_tit.place(x=0, y=20, height=18,width = 100)
d_hibrido=Label(f_csv, relief ='ridge',fg="black",bg="lightyellow", font=("Verdana",7))
d_hibrido.place(x=100, y=20, height=18)
d_hibrido_txt = StringVar()

d_bmv_tit=Label(f_csv, relief ='groove',text=" datos_bmv: ",font=("Verdana",7))
d_bmv_tit.place(x=0, y=40, height=18,width = 100)
d_bmv=Label(f_csv, relief ='ridge',fg="black",bg="lightyellow", font=("Verdana",7))
d_bmv.place(x=100, y=40, height=18)
d_bmv_txt = StringVar()

d_temp_tit=Label(f_csv, relief ='groove',text=" datos_ds18b20: ",font=("Verdana",7))
d_temp_tit.place(x=0, y=60, height=18,width = 100)
d_temp=Label(f_csv, relief ='ridge',fg="black",bg="lightyellow", font=("Verdana",7))
d_temp.place(x=100, y=60, height=18)
d_temp_txt = StringVar()

d_snre_tit=Label(f_csv, relief ='groove',text=" datos_snre: ",font=("Verdana",7))
d_snre_tit.place(x=0, y=80, height=18,width = 100)
d_snre=Label(f_csv, relief ='ridge',fg="black",bg="lightyellow", font=("Verdana",7))
d_snre.place(x=100, y=80, height=18)
d_snre_txt = StringVar()

################ FRAME PROGRAMAS ########################################

f_py = Frame(root,bg="khaki",width=240,bd=2,height=100)
f_py.place(x=455,y=80)# fill = BOTH)#,expand = True)

fv_py_tit=Label(f_py, relief ='groove',text=" En Ejecución ",font=("Verdana",7))
fv_py_tit.place(x=50, y=0, height=10,width = 100)

chat = Text(f_py, wrap='word', state='normal', width=70,font = ('Helvetica', 7, 'bold'))
chat.place(x=0, y=10, height=100)
p1 = subprocess.Popen(['ps','-eo','cmd'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', '-v','grep'], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen(['grep', 'python'], stdin=p2.stdout, stdout=subprocess.PIPE)
p2.stdout.close()  # permite a p2 recibir SIGPIPE si p3 existe.
p1.stdout.close()  # permite a p1 recibir SIGPIPE si p2 existe.
salida = p3.communicate()[0]
salida_py= salida.decode(encoding='UTF-8')

chat.insert("insert", salida_py)

################ FRAME PLACAS ########################################
f_placas = Frame(root,bg='skyblue',bd=2)#,width = 650,height = 150)
#frame1.pack(side = 'left' ,  fill="x")
f_placas.place(x=200, y=190, width = 350,height = 160)
#f_placas.pack(anchor= N,fill = Y, pady=10)#,expand = True)
#f_placas.pack(side= 'top',fill = NONE, ipady=5,ipadx=5,pady=5,padx=5,)#expand = True)

foto_sol = PhotoImage(file = './sol.gif') #148x148 pixels
canvas = Canvas(f_placas, width = 350,
                height = 150,confine=False,
                cursor =  'circle',bg='lightskyblue')#,bg = 'seagreen')
#canvas.pack(anchor = W,fill = Y)#, expand = True)
canvas.place(x=0,y=0)#,height=160,width = 160)
canvas.create_image(0, 0, anchor=NW,image=foto_sol)
canvas.create_text(250, 30,text = 'PLACAS', font = ('Helvetica', 22, 'bold'), fill='red')
canvas.update

Iplaca_status = Label(f_placas, relief ='sunken', width = 18)#.pack()
#Iplaca_status.pack(anchor = E,ipady=0,ipadx=0,pady=35,padx=5)
Iplaca_status.place(x=170,y=50)

Vplaca_status = Label(f_placas, relief ='groove', width = 18)
Vplaca_status.place(x=170,y=80)

Wplaca_status = Label(f_placas, relief ='ridge', width = 18)
Wplaca_status.place(x=170,y=110)


################ FRAME BATERIA ########################################

f_bat = Frame(root,bg='skyblue',bd=2,width = 400,height = 400)
f_bat.place(x=150, y=430, width = 460,height = 160)

foto_bateria = PhotoImage(file = 'bateria.gif') #148x148 pixels
canvas = Canvas(f_bat, width = 450,
                height = 150,confine=False,
                cursor =  'circle',bg='lightskyblue')#,bg = 'seagreen')
canvas.place(x=0,y=0)#,height=160,width = 160)
canvas.create_image(0, 0, anchor=NW,image=foto_bateria)
canvas.create_text(350, 30,text = 'BATERIA', font = ('Helvetica', 22, 'bold'), fill='red')
canvas.update

Vbat_status = Label(f_bat, relief ='sunken', width = 18)#.pack()
Vbat_status.place(x=270,y=50)

Ibat_status = Label(f_bat, relief ='groove', width = 18)
Ibat_status.place(x=270,y=80)

SOC_status = Label(f_bat, relief ='groove', width = 18)
SOC_status.place(x=270,y=110)


################ FRAME PWM / RELES ########################################

f_pwm = Frame(root,bg='skyblue',bd=2,width = 400,height = 400)
f_pwm.place(x=500, y=360, width = 160,height = 20)
#f_pwm.pack(side = 'right' )

pbar = ttk.Progressbar(f_pwm, style='text.Horizontal.TProgressbar', variable=variable)
pbar.pack()

################ FRAME CONSUMOS ########################################
f_consumo = Frame(root,bg='skyblue',bd=2)#,width = 200,height = 100)
f_consumo.place(x=0, y=360, width = 200,height = 30)
#f_consumo.pack(side = 'left' )

Wconsumo_status = Label(f_consumo, relief ='solid', width = 25)
Wconsumo_status.pack()
Wconsumo_status.configure(justify='left')

#########################################################3


def muestra():
    
    ##########  LECTURAS CSV ########################
    
    ### FV
    nombres=(['Tiempo_sg', 'Tiempo', 'Ibat','Vbat','SOC','DS','Aux1','Aux2',
    'Whp_bat','Whn_bat','Iplaca','Vplaca','Wplaca','Wh_placa',
    'Temp','PWM','Consumo','Mod_bat','Tabs','Tflot','Tflot_bulk',
    'SOC_min','SOC_max','Vbat_min','Vbat_max'])

    try:
        archivo_ram='/run/shm/datos_fv.json'
        with open(archivo_ram, 'rb') as f:
            dct = json.load(f)
        
        dct_fv={}
        for i in range (len(nombres)): dct_fv[nombres[i]]=dct[i]

        dif= time.time()- float(dct_fv['Tiempo_sg'])        
        if dif > 7: bg="yellow"
        else:       bg="green"
    except:
        bg="red"
        dct={'FV':'Error captura /run/shm/datos_fv'}
        print (time.strftime("%Y-%m-%d %H:%M:%S")+' - error lectura datos_fv')
        #time.sleep(5)    
    finally:
        d_fv.config(bg=bg)
        d_fv_txt.set(dct)
        d_fv.config(textvariable=d_fv_txt)
    
    
    ### HIBRIDO
    try:
        archivo_ram='/run/shm/datos_hibrido.pkl'
        with open(archivo_ram, 'rb') as f:
            dct = pickle.load(f)
        
        dif= time.time()- float(dct['Tiempo_sg'])        
        if dif > 7: bg="yellow"
        else:       bg="green"
    except:
        bg="red" 
        dct={'HIBRIDO':'Error captura /run/shm/datos_hibrido'}
    finally:
        d_hibrido.config(bg=bg)
        d_hibrido_txt.set(dct)
        d_hibrido.config(textvariable=d_hibrido_txt)


    ### BMV
    try:
        archivo_ram='/run/shm/datos_bmv.pkl'
        with open(archivo_ram, 'rb') as f:
            dct = pickle.load(f)
        
        dif= time.time()- float(dct['Tiempo_sg'])        
        if dif > 7: bg="yellow"
        else:       bg="green"
    except:
        bg="red" 
        dct={'BMV':'Error captura /run/shm/datos_bmv'}
    finally:
        d_bmv.config(bg=bg)
        d_bmv_txt.set(dct)
        d_bmv.config(textvariable=d_bmv_txt)

    
    ### DS18B20 TEMPERATURA
    try:
        archivo_ram='/run/shm/datos_ds18b20.pkl'
        with open(archivo_ram, 'rb') as f:
            dct = pickle.load(f)
        
        dif= time.time()- float(dct['Tiempo_sg'])        
        if dif > 7: bg="yellow"
        else:       bg="green"
    except:
        bg="red" 
        dct={'TEMP':'Error captura /run/shm/datos_ds18b20'}
    finally:
        d_temp.config(bg=bg)
        d_temp_txt.set(dct)
        d_temp.config(textvariable=d_temp_txt)
    
    ### SNRE
    try:
        archivo_ram='/run/shm/datos_snre.pkl'
        with open(archivo_ram, 'rb') as f:
            dct = pickle.load(f)
        
        dif= time.time()- float(dct['Tiempo_sg'])        
        if dif > 7: bg="yellow"
        else:       bg="green"
    except:
        bg="red" 
        dct={'SNRE':'Error captura /run/shm/datos_snre'}
    finally:
        d_snre.config(bg=bg)
        d_snre_txt.set(dct)
        d_snre.config(textvariable=d_snre_txt)
    
        
    #  ######### Programas activos #####
    if int(time.time())%10 == 0: #cada 10 sg
        p1 = subprocess.Popen(['ps','-eo','cmd'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-v','grep'], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(['grep', 'python'], stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()  # permite a p2 recibir SIGPIPE si p3 existe.
        p1.stdout.close()  # permite a p1 recibir SIGPIPE si p2 existe.
        salida = p3.communicate()[0]
        salida_py= time.strftime("    %Y-%m-%d -- %H:%M:%S")+'\n'+salida.decode(encoding='UTF-8')
        chat.delete("1.0","end")
        chat.insert("insert", salida_py)


    #  ###### Valores capturados ####

    if simular_datos==1:
        
        PWM = random.choice([0,10,20,30,40,50,60,70,80,90,100])
        PWM_t = "PWM= {0:>4,.1f} %".format(PWM).replace(",", "@").replace(".", ",").replace("@", ".")
 
        Ibat = random.choice([0,12,22,33,46,56,65,78,101,-10,-20,-30,-40,-50,-60,-70,-80.1,-90])
        Iplaca = random.choice([0,10,20,30,45,57,67,77,88,99,102,110])
        Vbat = random.choice([22.5,23.7,24.0,24.4,25.5,26.3,27,27.5,28.2,29.1])
        Vplaca = random.choice([60,59.4,61,59.9,52,60.1,61.6,58.7,62,57.3])
        Wplaca = random.choice([600,590.40,610,590.90,520,600.10,610.60,580.70,620,570.30])
        Temp = random.choice([10,12,14,16,18,20,22,24,26,28,30,32,34])
        Aux1 = random.choice([0,10,12,14,16,18,20,22,24,26,28,30,32,34])
        Aux2 = random.choice([0,10,12,14,16,18,20,22,24,26,28,30,32,34])
        SOC = random.choice([0,10,20,30,40,50,60,70,80,90,100]) 
        

        Consumo = Vbat * (Iplaca-Ibat)
        Consumo = "Wconsumo= {0:>9,.1f} W".format(Consumo).replace(",", "@").replace(".", ",").replace("@", ".")
    else:
        try:
            Ibat= float(dct_fv['Ibat'])
            Ibat_status.configure (bg='green')
            Ibat = "Ibat= {0:>5,.1f} A".format(Ibat).replace(",", "@").replace(".", ",").replace("@", ".")
        except:
            Ibat='Ibat= ERROR'
            Ibat_status.configure (bg='red')
        try:
            Vbat= float(dct_fv['Vbat'])
            Vbat_status.configure (bg='green')
            Vbat = "Vbat= {0:>5,.1f} V".format(Vbat).replace(",", "@").replace(".", ",").replace("@", ".")
        except:
            Vbat='Vbat= ERROR'
            Vbat_status.configure (bg='red')
        try:
            Iplaca= float(dct_fv['Iplaca'])
            Iplaca_status.configure (bg='green')
            Iplaca = "Iplaca= {0:>5,.1f} A".format(Iplaca).replace(",", "@").replace(".", ",").replace("@", ".")
        except:
            Iplaca='Iplaca= ERROR'
            Iplaca_status.configure (bg='red')
        try:
            Vplaca= float(dct_fv['Vplaca'])
            Vplaca_status.configure (bg='green')
            Vplaca = "Vplaca= {0:>5,.1f} V".format(Vplaca).replace(",", "@").replace(".", ",").replace("@", ".")
        except:
            Vplaca='Vplaca= ERROR'
            Vplaca_status.configure (bg='red')
        try:
            Wplaca= float(dct_fv['Wplaca'])
            Wplaca_status.configure (bg='green')
            Wplaca = "Wplaca= {0:>5,.1f} W".format(Wplaca).replace(",", "@").replace(".", ",").replace("@", ".")    
        except:
            Wplaca='Wplaca= ERROR'
            Wplaca_status.configure (bg='red')
        try:
            SOC= float(dct_fv['SOC'])
            SOC_status.configure (bg='green')
            SOC = "SOC= {0:>5,.1f} %".format(SOC).replace(",", "@").replace(".", ",").replace("@", ".")
        except:
            SOC='SOC= ERROR'
            SOC_status.configure (bg='red')
        try:
            PWM= float(dct_fv['PWM'])
            #PWM_status.configure (bg='green')
            PWM_t = "PWM= {0:>4,.1f} %".format(PWM).replace(",", "@").replace(".", ",").replace("@", ".")
        except:
            PWM=0
            PWM_t='PWM= ERROR'
        try:
            Consumo= float(dct_fv['Consumo'])
            Wconsumo_status.configure (bg='green')
            Consumo = "Wconsumo= {0:>5,.1f}".format(Consumo).replace(",", "@").replace(".", ",").replace("@", ".")
        except:
            Consumo='Consumo= ERROR'
            Wconsumo_status.configure (bg='red')
        
    try:    
        err=10
        Vbat_status.configure(text = Vbat);err=20
        Ibat_status.configure(text = Ibat);err=30
        SOC_status.configure(text = SOC);err=40
        
        Iplaca_status.configure(text = Iplaca);err=50
        Vplaca_status.configure(text = Vplaca);err=60
        Wplaca_status.configure(text = Wplaca);err=70
        Wconsumo_status.configure(text = Consumo);err=80
        
        if PWM > 0: print(PWM, PWM_t)
        pbar.step(PWM) ;err=90 # increment progressbar
        #style.configure('text.Horizontal.TProgressbar', 
        #                text='PWM {:g} %'.format(variable.get()))  # update label
        style.configure('text.Horizontal.TProgressbar', text=PWM_t)  # update label
    except:
        Vbat_status.configure (bg='red')
        Ibat_status.configure (bg='red')
        
        print (time.strftime("%Y-%m-%d %H:%M:%S")+' - error asignacion variables=',err)    
    root.after(t_refresco, muestra)

muestra()

root.mainloop()
