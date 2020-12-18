<?php
session_start([
    'cookie_lifetime' => 0,
]);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es-ES" lang="es-ES">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link href="img/favicon.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="css/index.css" rel="stylesheet" type="text/css" media="screen" />
    <title>RPi:Control sistema fotovoltaico</title>
</head>

<body>

    <div id="contenedor">
        <div id="cabecera">
            <a id="logo-header" href="index.php">
                <span class="site-name"><img src="img/fvcontrol.png" alt="logo" style="width:200px;height:60px;" /></span>
                
            </a> 
            <?php
            $recibe_pagina=$_GET['pagina'];
             ?>

            <nav>
                <ul>
                    <!-- Inicio -->
                    <li><a href="index.php?pagina=boton1" 
                        title="Inicio"><img src="img/Home.png" width="20" height="20"> Inicio</a>
                    </li>
                    
                    <!-- Utilidades -->
                    <li><a href="#" 
                        title="Utilidades"><img src="img/util.jpg" width="20" height="20"> Utilidades</a>
                        <ul>
                            <li><a href="index.php?pagina=meteo"
                                title="Gráficas Prevision Meteorologica">Meteorologia</a>
                            </li>
                            <li><a href="index.php?pagina=log"
                                title="Logs del sistema">Log</a>
                            </li>
                            
                        </ul>
                    </li>

                    <!-- Graficas -->
                    <li><a href="#"
                        title="Gráficas"><img src="img/Graph.png" width="20" height="20"> Gráficas</a>
                        <ul>
                            <li><a href="index.php?pagina=boton2"
                                title="KWh Red, Producción y Consumo">KWh</a>
                            </li>
                            <li><a href="index.php?pagina=boton3"
                                title="Promedios 30 días">Promedios</a>
                            </li>
                            <li><a href="index.php?pagina=botonH_temp"
                                title="Histórico temp">Hist_Temp</a>
                            </li>
                            <li><a href="index.php?pagina=botonH_horas"
                                title="Histórico 8 horas">Hist_8h</a>
                            </li>
                            <li><a href="index.php?pagina=botonH_1d"
                                title="Histórico 1 días">Hist_1</a>
                            </li>
                            <li><a href="index.php?pagina=botonH_3d"
                                title="Histórico 3 días">Hist_3</a>
                            </li>
                            <li><a href="index.php?pagina=botonH_mes"
                                title="Histórico Mes">Hist_Mes</a>
                            </li>
                            <li><a href="index.php?pagina=boton7"
                                title="Gráficas Producción y Consumo">Extra</a>
                            </li>
                            
                            <li><a href="index.php?pagina=boton8"
                                title="Tabla resumen diario">Diario</a>
                            </li>
                                                        
                        </ul>
                    </li>

                    <!-- Equipos -->
                    <li><a href="#" 
                        title="Equipos"><img src="img/inverter.png" width="20" height="20"> Equipos</a>
                        <ul>
                            <li><a href="index.php?pagina=botonH_hibrido"
                                title="Hibrido">Hibrido</a>
                            </li>
                            <li><a href="index.php?pagina=xxx"
                                title="Fronius">Fronius</a>
                            </li>
                            <li><a href="index.php?pagina=xxx"
                                title="Huawei">Huawei</a>
                            </li>
                            <li><a href="index.php?pagina=xxx"
                                title="SMA">SMA</a>
                            </li>
                            <li><a href="index.php?pagina=xxx"
                                title="BMV">BMV</a>
                            </li>
                        </ul>
                    </li>


                    <!-- Reles -->
                    <li><a href="#"
                        title="Relés"><img src="img/Target.png" width="20" height="20"> Relés</a>
                        <ul>
                            <li><a href="index.php?pagina=boton5"
                                title="Tabla relés">T.Relés</a>
                            </li>
                            <li><a href="index.php?pagina=boton6"
                                title="Horas funcionamiento">H.Relés</a>
                            </li>
                        </ul>
                    </li>
  
                    <!-- Celdas 
                    <li><a href="#"
                        title="Celdas"><img src="img/bateria.png" width="20" height="20"> Celdas</a>
                        <ul>
                            <li><a href="index.php?pagina=celda1"
                                title="Grafica diaria">Dia</a>
                            </li>
                            <li><a href="index.php?pagina=celda2"
                                title="Graficas resumen">Resumen</a>
                            </li>
                        </ul>
                    </li>
                    -->
                    
                </ul>
            </nav>
        </div>

    <div id="contenido">
        <br>
        <?php
            switch ($recibe_pagina){
                case "boton1":
                    include ("inicio_red.php");
                    break;
                case "boton2":
                    include ("wh_red.php");
                break;
                case "boton3":
                    include ("prom_30.php");
                    break;
                case "botonH_mes":
                    include ("historico_mes_red.php");
                    break;
                case "botonH_horas":
                    include ("historico_horas_red.php");
                    break;
                case "botonH_1d":
                    include ("historico1_red.php");
                    break;  
                case "botonH_3d":
                    include ("historico3c_red.php");
                    break;  
                case "botonH_hibrido":
                    include ("historico_hibrido.php");
                    break;                                  
                case "boton5":
                    include ("reles.php");
                    break;
                case "boton6":
                    include ("horas_reles.php");
                    break;
                case "boton7":
                    include ("grafica_elige.php");
                    break;
                case "boton8":
                    include ("diario.php");
                    break;
                case "log":
                    include ("log.php");
                    break;
                case "meteo":
                    include ("meteogram.php");
                    break;
                case "boton11":
                    include ("wh_2.php");
                    break;
                default:
                    include ("inicio_red.php");
            }
        ?>

        <br>
    </div>

</div>

</body>
</html>
