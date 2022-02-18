// ===========================================================================
// Pagina inicio.php  Actualizar segun los relojes y graficas que se usen 
// ===========================================================================

  // BAT ==   relojes que estan en opcion baterias
  // RED ==   relojes que estan en opcion RED
  // COMUN == relojes que estan siempre

    // BAT - Reloj Vbat
    Vbat_min = 44; 
    Vbat_bajo_amarillo = 48;
    Vbat_verde = 50.8;
    Vbat_alto_amarillo = 56;
    Vbat_alto_rojo = 60;
    Vbat_max = 64;
    
    // RED -Reloj Vred    
	Vred_min = 200; 
	Vred_bajo_amarillo = 210;
	Vred_verde = 215;
	Vred_alto_amarillo = 240;
	Vred_alto_rojo = 250;
	Vred_max = 270; 

    // BAT - SOC
    SOC_min=60;
    SOC_max=100;
    
    // RED - AC/DC EFICIENCIA
	EFF_min = 60;
	EFF_max = 100;


    // COMUN - Reloj Temp --- considerar que Temp_Vbat_xxx es realmente Temp_Inversor_xxx en sistemas sin bateria
    Temp_bat_min = -10;
    Temp_bat_baja = 10;
    Temp_bat_normal = 20;
    Temp_bat_alta = 30;
    Temp_bat_max = 50;

    Temp_rpi_min = 0;
    Temp_rpi_normal = 40;
    Temp_rpi_alta = 60;
    Temp_rpi_max = 100;

    // COMUN - Reloj Consumo y Autoconsumo en caso de RED
    Consumo_watios_min = 0;
    Consumo_watios_amarillo = 3000;
    Consumo_watios_rojo = 4000;
    Consumo_watios_max = 6000;
      
      //BAT - Aguja Reloj Iconsumo 
       Consumo_amperios_min= 0;
       Consumo_amperios_amarillo = 125;
       Consumo_amperios_rojo = 166;
       Consumo_amperios_max= 210;

    // BAT - Reloj Ibat/Iplaca
    Intensidad_min = -130;
    Intensidad_descarga_amarillo = -40;
    Intensidad_carga_rojo = 80;
    Intensidad_max = 130;

    // RED - Reloj Wred
	Wred_min = -5000;
	Wred_negativo_rojo = -2000;
	Wred_negativo_amarillo = -1000;
	Wred_positivo_amarillo = 500;
	Wred_positivo_rojo = 2000;
	Wred_max = 5000;
    
    
    // COMUN - Reloj Watios Placa
    Watios_placa_baja_rojo = 300;
    Watios_placa_verde = 3000;
    Watios_placa_alta_amarillo = 4500;
    Watios_placa_max = 6000;

    // COMUN - Reloj Vplaca
    Vplaca_baja_amarillo = 40;
    Vplaca_baja_verde = 50;
    Vplaca_verde = 60;
    Vplaca_alta_amarillo = 70;
    Vplaca_max = 80;

  // ==== GRAFICO CELDAS ====
    // BAT - Voltaje_celdas
    Vcelda_min = 1.7;
    Vcelda_max = 2.6;

    Vcelda_franja_min = 1.8;
    Vcelda_franja_max = 2.5;
    
    
  // === Grafico Tiempo Real en inicio.php ====
        // BAT 
        Escala_intensidad_min = -140;
        Escala_intensidad_max = 240;

        Escala_Vbat_min = 44;
        Escala_Vbat_max = 90;

            Vabs = 57.6;  // linea Vabs
            Vflot = 54.4; // Linea Vflot
        
        
        
        // Watios RED , CONSUMO, PLACA
        Escala_Wred_min = -5000;
        Escala_Wred_max = 6000;


        // COMUN
        Escala_Vplaca_max = 200;
        Escala_PWM_max = 2000; 
        


    // BAT - Tabla Colores Bateria
    SOC_max_rojo = 70;
    SOC_max_naranja = 80;

    SOC_min_rojo = 60;
    SOC_min_naranja = 75;

    Vbat_max_alta_rojo = 60;
    Vbat_max_alta_naranja = 58;
    Vbat_max_baja_rojo = 50;
    Vbat_max_baja_naranja = 54;

    Vbat_min_rojo = 44;
    Vbat_min_naranja = 46;
    
    
    // RED - Tabla Colores  RED
	  
	EFF_max_rojo = 70;
	EFF_max_naranja = 80;

	EFF_min_rojo = 60;
	EFF_min_naranja = 75;
    
	Vred_max_alta_rojo = 245;
	Vred_max_alta_naranja = 240;
	Vred_max_baja_rojo = 205;
	Vred_max_baja_naranja = 215;

	Vred_min_rojo = 205;
	Vred_min_naranja = 215;
    
    // Variables Auxilares
    Nombre_Aux1 = 'Aux1';
    Unidades_Aux1 = '';
    
    Nombre_Aux2 = 'Aux2';
    Unidades_Aux2 = '';
    
    Nombre_Aux3 = 'Aux3';
    Unidades_Aux3 = '';
    
    Nombre_Aux4 = 'Aux4';
    Unidades_Aux4 = '';
    
    Nombre_Aux5 = 'Aux5';
    Unidades_Aux5 = '';
    
    Nombre_Aux6 = 'Aux6';
    Unidades_Aux6 = '';
    
    Nombre_Aux7 = 'Aux7';
    Unidades_Aux7 = '';

        
// Pagina Historico1.php,  Historico_horas.php, historico_con_temp.php  ........

    // Se usan los mismos datos puestos en grafica tempo real de inicio.php mas los siguientes parametros:
    
    
    Escala_Vred_min = 180;
    Escala_Vred_max = 280;

        
    Kwh_placa_max = 35;
    
    Kwh_bat_min = -10;
    Kwh_bat_max = 10;
    
    Kwh_red_min = -30;
    Kwh_red_max = 30;
    
    Kwh_consumo_min = 0;
    Kwh_consumo_max = 35;
    
    Temp_min = -10;
    Temp_max = 60;
    
    Modo_max = 20;  // 1= OFF, 2=BULK, 3= FLOT, 4= ABS,  5= EQU, 6= INYEC.RED, 7= CONSUMO RED
    
    Aux1_min = 0;
    Aux1_max = 100;
    
    Aux2_min = 0;
    Aux2_max = 100;
    
    
    // Poner a true si se quiere que aparezcan los ejes en la grafica o false para que no aparezcan
    Eje_Intensidad = true; // Eje Ibat e Iplaca
    Eje_Vbat = true;
    Eje_SOC = false;
    Eje_PWM = false;
    
    Eje_Vplaca = false;
    Eje_Wplaca = false;
    Eje_Wred = false;
    Eje_Vred = false;
    Eje_Wconsumo = false;
    
    Eje_Kwh_placa = false;
    Eje_Kwh_bat = false;
    Eje_Kwh_red = false;
    Eje_Kwh_consumo = false;
    
    Eje_Temp = false;
    Eje_Modo = false;
    
    Eje_Aux1 = false;
    Eje_Aux2 = false;
    
    // Poner a true si se quiere que se muestre la grafica por defecto o false para que salga como desactivada
    Ibat_visible = true;
    Iplaca_visible = true;
    Vbat_visible = true;
    SOC_visible = true;
    PWM_visible = true;
    
    Vplaca_visible = false;
    Wplaca_visible = false;
    Wred_visible = false;
    Wconsumo_visible = false;
    Vred_visible = false;
    
    Kwh_placa_visible = false;
    Kwh_bat_visible = false;
    Kwh_red_visible = false;
    Kwh_consumo_visible = false;
    
    Temp_visible = false;
    Modo_visible = true;
    
    Aux1_visible = false;
    Aux2_visible = false;
    
