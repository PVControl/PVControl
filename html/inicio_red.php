<?php

// Se debe interpretar Vbat/Ibat/SOC como Vred/Ired/EFF  
// se han mantenido los nombres por simplicacion de cambios entre FV con o sin Baterias

require('conexion.php');
//Coger datos grafica tiempo real
$sql = "SELECT UNIX_TIMESTAMP(Tiempo)*1000 as Tiempo,  Ibat, Iplaca, Vbat, PWM, Vplaca
        FROM datos WHERE Tiempo >= (NOW()- INTERVAL 3 MINUTE)
        ORDER BY Tiempo";

if($result = mysqli_query($link, $sql)){

  $i=0;
  while($row = mysqli_fetch_assoc($result)) {
        //guardamos en rawdata todos los vectores/filas que nos devuelve la consulta
        $rawdata3[$i] = $row;
        $i++;
  }
} else{
        echo "ERROR: No se puede ejecutar $sql. " . mysqli_error($link);
}

mysqli_close($link);

?>

<HTML>

<head>
<link href="css/inicio.css" rel="stylesheet" type="text/css" media="screen" />
<style type="text/css">
body {
color: purple;

background: linear-gradient(to bottom, white, #fafafa);}
</style>

</head>


<body>

<meta charset="utf-8">

<!-- Importo el archivo Javascript de Highcharts directamente desde la RPi 
<script src="js/jquery.js"></script>

<script src="js/highcharts.js"></script>
<script src="js/highcharts-more.js"></script>
<script src="js/highcharts-3d.js"></script>

<script src="js/themes/grid.js"></script>

<script src="js/modules/solid-gauge.js"></script>
<script src="http://code.highcharts.com/themes/grid.js"></script>
-->


<script src="Parametros_Web.js"></script>



<!-- Latest compiled and minified JavaScript -->
<script src="https://code.jquery.com/jquery.js"></script>

<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="http://code.highcharts.com/highcharts-more.js"></script>
<script src="https://code.highcharts.com/highcharts-3d.js"></script>

<script src="http://code.highcharts.com/themes/grid.js"></script>
<script src="https://code.highcharts.com/modules/solid-gauge.js"></script>


<!--<div id="grafica_intensidad" style="width: 25%; height: 260px; margin-left: -25%; margin-top: 260px;margin-right: 0%; float: left"></div>-->
<div class="divTable"style="color:black; width: 10%; height: 350px; margin-left: 1%; margin-right:2%;margin-top: -1%; margin-bottom: 0%; float: left">
    <div class="divTableBody">
        <div class="divTableRow">
                <div class="divTableCell">Wh Placa</div>
                <div id= "Wh_placa" class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">Wh Cons</div>
            <div id= "Wh_Cons" class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">Wh Red+</div>
            <div id= "Whp_bat" class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">Wh Red-</div>
            <div id= "Whn_bat" class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">&nbsp;EFF máx</div>
            <div id = "maxSOC" class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">EFF mín</div>
            <div id ="minSOC" class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">&nbsp;Vred mín</div>
            <div id = "minVbat" class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">&nbsp;Vred máx</div>
               <div id ="maxVbat" class="divTableCell">&nbsp;</div>
            </div>
        <div class="divTableRow">
            <div class="divTableCell"></div>
            <div class="divTableCell">&nbsp;</div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">Estado</div>
            <div id ="Mod_bat" class="divTableCell">&nbsp;</div>
        </div>
        </div>
    </div>
</div>

<div id="containervbat"  style="width: 20%; height: 180px; margin-left: 2%; margin-right: 0%;margin-top: -1%; float: left">
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  </div>
<div id="containeribat"  style="width: 20%; height: 180px; margin-left: 0%; margin-top: -1%; float: left"></div>
<div id="containertemp"  style="width: 20%; height: 180px; margin-left: 0%; margin-top: -1%; float: left"></div>
<div id="containervplaca"  style="width: 20%; height: 180px; margin-left: 0%; margin-top: -1%; float: left"></div>

<div id="containerSOC"  style="width: 23%; height: 180px; margin-bottom: 0%; margin-left: 9%;margin-top: -2%; float: left"></div>
<div id="containerconsumo"  style="width: 20%; height: 180px; margin-left: 0%; margin-top: 0%;margin-top: -2%; float: left"></div>
<div id="containerwplaca"  style="width: 20%; height: 180px; margin-left: 0%; margin-top: 0%;margin-top: -2%; float: left"></div>


<div id="container_reles" style="width: 80%; height: 160px; margin-left: 1%;float: left"></div>


<div id="grafica_intensidad" style="width: 100%; height: 280px; margin-left: 0%; margin-bottom: 0% ;float: left"></div>

<!--
<script src='https://openweathermap.org/themes/openweathermap/assets/vendor/owm/js/d3.min.js'></script>

<script>window.myWidgetParam ? window.myWidgetParam : window.myWidgetParam = []; 
 window.myWidgetParam.push({id: 11,cityid: '6359366',appid: '755658d8a95ced40e5fd850f33183f9d',units: 'metric',containerid: 'openweathermap-widget-11',  }); 
 (function() {var script = document.createElement('script');script.async = true;script.charset = "utf-8";
 script.src = "https://openweathermap.org/themes/openweathermap/assets/vendor/owm/js/weather-widget-generator.js";
 var s = document.getElementsByTagName('script')[0];s.parentNode.insertBefore(script, s);  })();
 </script>

<div id="openweathermap-widget-11"></div>
-->


<br>
<br style="clear:both;"/>
<br>

</body>

<script>


$(function () {
    
    recibirDatosFV(); 

    
    Highcharts.setOptions({
        
        global: {
           useUTC: false
           },
        lang: {
            months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            weekdays: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
            shortMonths: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
            rangeSelectorFrom: "Desde",
            rangeSelectorTo: "A",
            printChart: "Imprimir gráfico",
            loading: "Cargando..."
            } 
        });

    chart_vbat = new Highcharts.Chart ({
        chart: {
            renderTo: 'containervbat',
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null,
            },
        title: {
            y:155,
            floating: true,
            /*style:{
                color: 'Purple',
                fontSize:'18px',
                },*/
            text: 'Vred',
            },
        subtitle: {
            y:60,
            floating: true,
            text: '',
          },
        credits: {
            enabled: false
            },
        pane: {
            size: '105%',
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                        ]
                    },
                borderWidth: 0,
                //outerRadius: '109%' - orla
                outerRadius: '100%'
                }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                        ]
                    },
                borderWidth: 0,
                outerRadius: '100%'
                }, {
                // default background
                }, {
                backgroundColor: null,//#DDD
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
                
                }]
            },
        yAxis: {
            min: Vbat_min,
            max: Vbat_max,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 1,
                rotation: 'auto'
              },
            title: {
                y:10,//-30,
                x:0,
                floating:true,
                reserveSpace:false,
                style: {
                   fontSize: '16px'
                  },
                text: 'pp1' //'V_BAT'
                },
            subtitle: {
                y:50,//-30,
                x:0,
                floating:true,
                reserveSpace:false,
                style: {
                   fontSize: '16px'
                  },
                text: 'pp2' //null //'V_BAT'
                },
                
            plotBands: [
              {
                from: Vbat_min,
                to: Vbat_bajo_amarillo,
                color: '#DF5353' // red
              },
              {
                from: Vbat_bajo_amarillo,
                to: Vbat_verde,
                color: '#DDDF0D' // yellow
              },
              {
                from: Vbat_verde,
                to: Vbat_alto_amarillo,
                color: '#55BF3B' // green
              },
              {
                from: Vbat_alto_amarillo,
                to: Vbat_alto_rojo,
                color: '#DDDF0D' // yellow
              },
          
              {
                from: Vbat_alto_rojo,
                to: Vbat_max,
                color: '#DF5353' // red
              }]
            },
        navigation: {
            buttonOptions: {
                enabled: false
              }
          },
        tooltip: {
            enabled: false
          },
        series: [{
            name: 'Vred',
            data: [],
            dataLabels: {
                enabled: true,
                allowOverlap: true,
                borderWidth: 0,
                y: 0,
                style: {
                   fontSize: '18px'
                  },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,2) + " V"
                    },
              }
          }]
        });
    
    chart_soc = new Highcharts.Chart ({
        chart: {
            renderTo: 'containerSOC',
            type: 'solidgauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null
            
            //
          },
        title: {
            y:140,
            widthAdjust: 0,
            style: {
                fontSize: '30px'
                },
            floating: true,
            text: 'DC/AC EFICIENCIA INVERSOR'
          },
        credits: {
            enabled: false
          },
        pane: {
            center: ['50%', '65%'],
            size: '130%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '100%',
                outerRadius: '100%',
                shape: 'arc'
              }
          },
        tooltip: {
            enabled: false
          },
        yAxis: {
            min: SOC_min,
            max: SOC_max,
            stops: [
                [0.6,'rgba(223,83,83,0.7)' ], // red'#DF5353'
                [0.7, 'rgba(221,223,13,0.7)'], // yellow'#DDDF0D'
                [0.85, 'rgba(85,191,59,0.7)'] // green'#55BF3B'
              ],
            lineWidth: 1,
            minorTickInterval: 1, //null,
            tickAmount: 9,
            
            //title: {
            //    y: -30
            // },
             
            title: {
                y: 80,//-30,
                floating: true,
                //align: 'right',
                //verticalAlign: 'bottom',
                //x:0,
                style: {
                   fontSize: '15px'
                  },
                text: '' //null //'V_BAT'
                },
            
            labels: { // valores de la escala
                y: 0,
                min: SOC_min,
                max: SOC_max,
              }, // valores max y min
            //title: {
                //y: -50,
            //  text: null
             //},

          },
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 35,    // Valor dato
                    borderWidth: 2,
                    useHTML: true
                  }
             }
          },
        navigation: {
            buttonOptions: {
                enabled: false
              }
          },
        series: [{
            name: '%',
            
            title: {
                floating:true,
                y:150,//-30,
                x:0,
                text: 'HOLA', //null //'V_BAT'
                style: {
                   fontSize: '15px'
                  },
                },
            
            data: [],
            dataLabels: {
                y:-35,
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                  ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span>' +
                       '<span style="font-size:15px;color:silver">%</span></div>'
              },
          }]
      });
    
    chart_temp = new Highcharts.Chart ({
        chart: {
            renderTo: 'containertemp',
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null
          },
        title: {
            y:155,
            floating: true,
            text: 'Temp',
          },
        credits: {
            enabled: false
          },   
        pane: [{
            size: '105%',
            startAngle: -150,
            endAngle: -10,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                      ]
                  },
                borderWidth: 0,
                //outerRadius: '109%' - orla
                outerRadius: '100%'
              }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                      ]
                  },
                borderWidth: 1,
                outerRadius: '105%'
              }, {
                // default background
              }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
              }]

          }, {
            size: '105%',
            startAngle: 20,
            endAngle: 150,
            background: []
          }],
            // the value axis
        yAxis: [{
            min: Temp_bat_min,
            max: Temp_bat_max,

            minorTickInterval: 5,
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',

            tickPixelInterval: 30,
            tickInterval: 10,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',

            title: {
                y: 10,
                text: null, //'TEMP.'
              },
                
            labels: {
                allowOverlap:true,
                step: 1,
                rotation: 'auto'
              },
                
            plotBands: [{
                from: Temp_bat_normal,
                to: Temp_bat_alta,
                color: '#55BF3B' // green
              
               },{
                from: Temp_bat_baja,
                to: Temp_bat_normal,
                color: '#DDDF0D' // yellow
              },{
                from: Temp_bat_min,
                to: Temp_bat_baja,
                color: '#3C14BF' // blue
              }, {
                from: Temp_bat_alta,
                to: Temp_bat_max,
                color: '#DF5353' // red
              }]
          }, {    
            reversed: true,
            min: Temp_rpi_min,
            max: Temp_rpi_max,
            pane: 1,
            minorTickInterval: 10,
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',

            tickPixelInterval: 30,
            tickInterval: 20,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
                
            labels: {
                allowOverlap:true,
                step: 1,
                rotation: 'auto'
              },

            plotBands: [{
                from: Temp_rpi_min,
                to: Temp_rpi_normal,
                color: '#55BF3B' // green
              }, {
                from: Temp_rpi_normal,
                to: Temp_rpi_alta,
                color: '#DDDF0D' // yellow
              }, {
                from: Temp_rpi_alta,
                to: Temp_rpi_max,
                color: '#DF5353' // red
              }]
 
          }],
        navigation: {
            buttonOptions: {
                enabled: true
              }
          },
        tooltip: {
            enabled: true
          },
        series: [{
            yAxis: 0,
            name: 'TEMP',
            data: [],
            dataLabels: {
                allowOverlap: true,
                enabled: true,
                borderWidth: 0,
                y: -35, //-35,
                x: 0,
                style: {
                    fontSize: '15px'
                  },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,1) + "ºC Inv"
                  }
              },
            dial: {
                backgroundColor : 'black',   //Color de la aguja
                radius: '80%' //longitud de la aguja
              },
          },{
            yAxis: 1,
            name: 'CPU',
            data: [],
            dataLabels: {
                allowOverlap: true,
                enabled: true,
                borderWidth: 0,
                y: 20, //10,
                x: 0,
                style: {
                    fontSize: '15px',
                    color: 'red'
                  },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,0) + "ºC Rpi"
                  }
              },
            dial: {
                backgroundColor : 'red',   //Color de la aguja
                radius: '80%' //longitud de la aguja
              },
          }]        
      });
    
    chart_consumo = new Highcharts.Chart ({
        chart: {
            renderTo: 'containerconsumo',
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            alignTicks: false,
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null
          },
        title: {
            y:155,
            floating: true,
            text: 'Consumo',
          },
        subtitle: {
            y:42,
            floating: true,
            text: '',
          },
        credits: {
            enabled: false
          },
        pane: [{
            size: '105%',
            startAngle: -150,
            endAngle: -10,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                      ]
                  },
                borderWidth: 0,
                //outerRadius: '109%' - orla
                outerRadius: '100%'
              }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                      ]
                  },
                borderWidth: 0,
                outerRadius: '100%'
              }, {
                // default background
              }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
              }]

          }, {
            size: '105%',
            startAngle: 10,
            endAngle: 150,
            background: []
          }],

            
        yAxis: [
          { // Wconsumo
            min: Consumo_watios_min,
            max: Consumo_watios_max,
            pane: 0,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickInterval: 1000,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            title: {
                y: 10,
                text: null, //'CONSUMO'
              },
            labels: {
                allowOverlap:true,
                step: 1,
                rotation: 'auto'
              },
            plotBands: [{
                from: Consumo_watios_min,
                to: Consumo_watios_amarillo,
                color: '#55BF3B' // green
              }, {
                from: Consumo_watios_amarillo,
                to: Consumo_watios_rojo,
                color: '#DDDF0D' // yellow
              }, {
                from: Consumo_watios_rojo,
                to: Consumo_watios_max,
                color: '#DF5353' // red
              }]
          },
          { // Aconsumo
            reversed: true,
            min: Consumo_amperios_min,
            max: Consumo_amperios_max,
            pane: 1,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickInterval: Consumo_amperios_max/5,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                allowOverlap:true,
                step: 1,
                rotation: 'auto'
              },
            plotBands: [{
                from: Consumo_amperios_min,
                to: Consumo_amperios_amarillo,
                color: '#55BF3B' // green
              }, {
                from: Consumo_amperios_amarillo,
                to: Consumo_amperios_rojo,
                color: '#DDDF0D' // yellow
              }, {
                from: Consumo_amperios_rojo,
                to: Consumo_amperios_max,
                color: '#DF5353' // red
              }]
          }
          ],
        
        navigation: {
            buttonOptions: {
                enabled: false
              }
          },
        tooltip: {
            enabled: false
          },
        series: [
          { // WConsumo
            yAxis: 0,
            name: 'Consumo W',
            data: [],
            dataLabels: {
                allowOverlap:true,
                enabled: true,
                borderWidth: 0,
                y: -35,
                x: 0,
                style: {
                    fontSize: '15px'
                  },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,0) + "W"
                  }
              },
            dial: {
                backgroundColor : 'black',   //Color de la aguja
                radius: '80%' //longitud de la aguja
              },
          },
          { //Aconsumo
            yAxis: 1,
            name: '',
            data: [],
            dataLabels: {
                allowOverlap:true,
                enabled: true,
                borderWidth: 0,
                y: 20,
                x: 0,
                style: {
                    fontSize: '15px',
                    color : 'red'
                  },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,0) + "A"
                  }
              },
            dial: {
                backgroundColor : 'red',   //Color de la aguja
                radius: '80%' //longitud de la aguja
              },
          }
          ]        
      });
    
    
    chart_ibat = new Highcharts.Chart ({ // Valor Excedentes (Ired * Vred) realmente  en FV SIN bateria
        chart: {
            renderTo: 'containeribat',
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null
            },
        title: {
            y:155,
            floating:true,
            text: 'Excedentes',
            style: {
                fontSize: '12px',
                color: 'black'
                },
            },
        subtitle: {
            y:165,
            floating:true,
            text: '',
            style: {
                fontSize: '14px',
                color: 'green'
                },
            },
                       
        credits: {
                enabled: false
            },
        pane: {
                size: '105%',
                startAngle: -150,
                endAngle: 150,
                background: [{
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#FFF'],
                            [1, '#333']
                        ]
                    },
                    borderWidth: 0,
                    //outerRadius: '109%' - orla
                    outerRadius: '100%'
                }, {
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#333'],
                            [1, '#FFF']
                        ]
                    },
                    borderWidth: 0,
                    outerRadius: '100%'
                }, {
                    // default background
                    //backgroundColor: 'red'
                }, {
                    backgroundColor: '#DDD',
                    borderWidth: 0,
                    outerRadius: '105%',
                    innerRadius: '103%'
                 }]
            },
        yAxis: {
                min: Intensidad_min,
                max: Intensidad_max,

                minorTickInterval: 'auto',
                minorTickWidth: 1,
                minorTickLength: 2,
                minorTickPosition: 'inside',
                minorTickColor: '#666',

                tickPixelInterval: 30,
                tickWidth: 2,
                tickPosition: 'inside',
                tickLength: 10,
                tickColor: '#666',
                labels: {
                    step: 2,
                    rotation: 'auto'
                },
                title: {
                    y:20,
                    text: null, //'I_BAT'
                    
                },
                plotBands: [{
                    from: 0,
                    to: Intensidad_carga_rojo,
                    color: '#55BF3B' // green
                }, {
                    from: Intensidad_descarga_amarillo,
                    to: 0,
                    color: '#DDDF0D' // yellow
                }, {
                    from: Intensidad_min,
                    to: Intensidad_descarga_amarillo,
                    color: '#DF5353' // red
                }, {
                    from: Intensidad_carga_rojo,
                    to: Intensidad_max,
                    color: '#DF5353' // red
                }]
            },
        navigation: {
            buttonOptions: {
                enabled: false
            }
        },
        
        tooltip: {
                  enabled: false
                 },

        series: [{
            name: 'Excedentes',
            data: [],
            dataLabels: {
                allowOverlap:true,
                enabled: true,
                borderWidth: 0,
                y: 10,
                style: {
                    fontSize: '20px',
                    color: 'black'
                    },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,1) + " W"
                    },
                },
            dial: {
                backgroundColor: (([this.y] <= 0) ? 'red' : 'green')
                }
            } /* 
            ,{
            name: 'Iplaca',
            data: [],
            dataLabels: {
                allowOverlap:true,
                enabled: true,
                borderWidth: 0,
                y: 12,
                style: {
                    fontSize: '14px',
                    color: 'green'
                    },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,1) + " W"
                    },
                },
            dial: {
                backgroundColor: (([this.y] <= 0) ? 'green' : 'red')
                }

             }
             */
            ]
        });
    
    chart_wplaca = new Highcharts.Chart ({
        chart: {
            renderTo: 'containerwplaca',
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null
            },
        title: {
            y:155,
            floating:true,
            text: 'Wplaca',
            },
        credits: {
                enabled: false
            },
        pane: {
                size: '105%',
                startAngle: -150,
                endAngle: 150,
                background: [{
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#FFF'],
                            [1, '#333']
                        ]
                    },
                    borderWidth: 0,
                    //outerRadius: '109%' - orla
                    outerRadius: '100%'
                }, {
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#333'],
                            [1, '#FFF']
                        ]
                    },
                    borderWidth: 0,
                    outerRadius: '100%'
                }, {
                    // default background
                }, {
                    backgroundColor: '#DDD',
                    borderWidth: 0,
                    outerRadius: '105%',
                    innerRadius: '103%'
                 }]
            },
        yAxis: {
            min: 0,
            max: Watios_placa_max,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickInterval: 1000,
            tickWidth: 1,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                allowOverlap:true,
                step: 1,
                rotation: 'auto'
            },
            title: {
                y:20,//-30,
                x:0,
                style: {
                   fontSize: '16px'
                  },
                text: '' //null 
                },
            
        plotBands: [{
                    from: 0,
                    to: Watios_placa_baja_rojo,
                    color: '#DF5353' // red
                }, {
                    from: Watios_placa_baja_rojo,
                    to: Watios_placa_verde,
                    color: '#55BF3B' // green
                }, {
                    from: Watios_placa_verde,
                    to: Watios_placa_alta_amarillo,
                    color: '#DDDF0D' // yellow
                }, {
                    from: Watios_placa_alta_amarillo,
                    to: Watios_placa_max,
                    color: '#DF5353' // red
                }]
            },
        navigation: {
            buttonOptions: {
                enabled: false
            }
        },

        tooltip: {
                  enabled: false
                 },
        series: [{
            name: 'Wplaca',
            data: [],
            dataLabels: {
                allowOverlap:true,
                enabled: true,
                borderWidth: 0,
                y: 10,                   
                style: {
                    fontSize: '20px'                        
                    },
                formatter: function() {
                     return Highcharts.numberFormat(this.y,0) + " W"
                    },
                }
            }]
        });
    chart_vplaca = new Highcharts.Chart ({
        chart: {
            renderTo: 'containervplaca',
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null,
            },
        title: {
            y:155,
            floating: true,
            style: {
                    color: 'Black',
                    fontWeight: 'bold',
                    fontSize:'18px',
                },
            text: 'Vplaca',
            },
        credits: {
            enabled: false
            },
        pane: {
            size: '105%',
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                        ]
                    },
                borderWidth: 0,
                //outerRadius: '109%' - orla
                outerRadius: '100%'
                }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                        ]
                    },
                borderWidth: 0,
                outerRadius: '100%'
                }, {
                // default background
                }, {
                backgroundColor: '#DDD',//#DDD
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
                }]
            },
        yAxis: {
            min: 0,
            max: Vplaca_max,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
           
            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
              },
            title: {
                y:20,//-30,
                x:0,
                reserveSpace:false,
                style: {
                   fontSize: '16px'
                  },
                text: '' //null //'V_BAT'
                },
            subtitle: {
                y:0,//-30,
                x:-30,
                style: {
                   fontSize: '10px'
                  },
                text: 'pp' //null //'V_BAT'
                },
                
            plotBands: [{
                from: 0,
                to: Vplaca_baja_amarillo,
                color: '#DDDF0D' // amarillo
              }, {
                from: Vplaca_baja_amarillo,
                to: Vplaca_baja_verde,
                color: '#d5f09d' // low green
              }, {
                from: Vplaca_baja_verde,
                to: Vplaca_verde,
                color: '#55BF3B' // green
              }, {
                from: Vplaca_verde,
                to: Vplaca_alta_amarillo,
                color: '#DDDF0D' // amarillo
              }, {
                from: Vplaca_alta_amarillo,
                to: Vplaca_max,
                color: '#DF5353' // red
              }]
            },
        navigation: {
            buttonOptions: {
                enabled: false
              }
          },
        tooltip: {
            enabled: false
          },
        series: [{
            name: 'Vplaca',
            data: [],
            dataLabels: {
                enabled: true,
                allowOverlap: true,
                borderWidth: 0,
                y: 10,
                style: {
                   fontSize: '20px'
                  },
                formatter: function() {
                    return Highcharts.numberFormat(this.y,1) + " V"
                    },
              }
          }]
        });
                            
    chart_reles =new Highcharts.Chart({
        chart: {
            renderTo: 'container_reles',
            backgroundColor: null,//'#ffffff',//'#f2f2f2',
            borderColor: null,
            type: 'column',
            shadow: false,
            options3d: {
                enabled: true,
                alpha: 0,
                beta: 10,
                depth: 100,
                viewDistance: 25,
            //backgroundColor: null,//'#ffffff',//'#f2f2f2',
            //borderColor: null,
           
            },
            
        },
        
        plotOptions: {
          column: {
            dataLabels: {
                enabled: true,
                inside: true, //valor de la columna en el interior
                crop: false,
                overflow: 'none',
                //borderWidth: null,
                //borderColor: 'red',
            },
            enableMouseTracking: false
          }
        },

        
        credits: {
             enabled: false
             },
        title: {
              y:20,
              text: 'SITUACION RELES'
             },
        subtitle: {
              text: null
             },
        xAxis: {
             categories: [] //Nombre_Reles()
               },
        yAxis: {
              gridLineWidth: 0,
              minorGridLineWidth: 0,
              gridLineColor: 'transparent',
              min: 0,
              max: 100,
              //minPadding:0,
              //maxPadding:0,
              tickInterval: 10,
              allowDecimals: false,
              visible: true, //desactivar grid i resta
              labels: {
                    enabled: true
               },
              title: {
                    enabled: false
               }
              
             },

        series: [{
                name: 'Estado Relés',
                colorByPoint: false,//Color aleatorio para cada columna de un rele
                color : '#2b5dc7',
                borderColor: '#303030',
                data: [],
                
                dataLabels: {
                    enabled: true, 
                    formatter: function() {
                        return Highcharts.numberFormat(this.y,0) + " %"
                    }
                }

                }],
        
        navigation: {
              buttonOptions: {
                enabled: false
               }
             },
        legend: {
              enabled: false,
              layout: 'vertical',
              floating: true,
              align: 'center',
              verticalAlign: 'center',
              //x: -100,
              y: 30,
              borderWidth: 0
             },
        tooltip: {
              formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    this.point.y + ' ' + this.point.name.toLowerCase();
               }
             }

      });
 
  
    grafica_i = new Highcharts.Chart ({
        chart: {
         renderTo: 'grafica_intensidad',
         backgroundColor: null,//'#ffffff',//'#f2f2f2',
         borderColor: null,
         plotBorderWidth: 1,
         zoomType: 'xy',
         alignTicks: false,
         animation: Highcharts.svg, // don't animate in old IE
         //marginRight: 10,
               },
       title: {
            text: '',
            floating:true,
            y: 12,
            x:-0
            },
        subtitle: {
            text: 'Prueba Dinamica',
            floating:true,
            align: 'right',
            verticalAlign: 'bottom',
            y: 25,
            
            },
        credits: {
            enabled: false
            },
        xAxis: {
            type: 'datetime'
            },
        yAxis: [{
            gridLineWith: 2,
            min: Escala_intensidad_min,
            max: Escala_intensidad_max,
            opposite: true,
            tickInterval:40,
            gridLineColor: 'transparent',
            minorGridLineColor: 'transparent',
            //endOnTick: true,
            //maxPadding: 0.2,
            //tickAmount: 7,
            labels: {
                //format: '{value} A',
                style: {
                    color: Highcharts.getOptions().colors[2]
                    }
                },
            title: {
                text: null,
                },
            //opposite: false,
            },{
            
            // ########## Valores eje Vbat ######################
            opposite: false,
            min: Escala_Vbat_min,
            max: Escala_Vbat_max,
            tickInterval: 1,
            //gridLineColor: 'transparent',
            minorGridLineColor: 'transparent',
            labels: {
                format: '{value} V',
                style: {
                    color: Highcharts.getOptions().colors[0]
                    }
                },
            title: {
                text: '',
                },
            plotLines: 
              [{ // ########## Valores Linea Vabs #####################
                value: Vabs,
                width: 2,
                color: 'green',
                dashStyle: 'shortdash',
                label: {
                    text: 'Vabs'
                    }
                },
                {// ########## Valores Linea Vflot ######################
                value: Vflot,
                width: 2,
                color: 'red',
                dashStyle: 'shortdash',
                label: {
                    text: 'Vflot'
                    }
              }]
            },{
            
            // ########## Valores eje PWM ######################
            opposite: true,
            min: 0,
            max: Escala_PWM_max,
            tickInterval: 20,
            gridLineColor: 'transparent',
            minorGridLineColor: 'transparent',
            
            title: {
                text: '',
                },
            },{
            
            // ########## Valores eje Vplaca ######################
            opposite: false,
            min: 0,
            max: Escala_Vplaca_max,
            tickInterval: 20,
            gridLineColor: 'transparent',
            minorGridLineColor: 'transparent',
            
            title: {
                text: '',
                },
            }
            
            
            ],
          
        tooltip: {
            crosshairs: true,
            shared: true,
            valueDecimals: 2
            },
        navigation: {
            buttonOptions: {
                enabled: false
                }
            },
        plotOptions: {
            series: {
                marker: {
                    enabled: false
            }
        }
        },

        legend: {
            layout: 'horizontal',
            floating: true,
            align: 'left',
            verticalAlign: 'bottom',
            //x: -100,
            y: 20,
            borderWidth: 0
            },
        series: [
        {name: 'Ibat',
            yAxis: 0,
            color: Highcharts.getOptions().colors[2],
            data: (function() {
                var data = [];
                <?php
                for($i = 0 ;$i<count($rawdata3);$i++){
                ?>
                    data.push([<?php echo $rawdata3[$i]["Tiempo"];?>,<?php echo $rawdata3[$i]["Ibat"];?>]);
                <?php } ?>
              return data;
              })()

            },
        
        {name: 'IPlaca',
            yAxis: 0,
            color: Highcharts.getOptions().colors[3],
            data: (function() {
                var data = [];
                <?php
                for($i = 0 ;$i<count($rawdata3);$i++){
                ?>
                    data.push([<?php echo $rawdata3[$i]["Tiempo"];?>,<?php echo $rawdata3[$i]["Iplaca"];?>]);
                <?php } ?>
              return data;
              })()

            },
            {name: 'Vbat',
            color: Highcharts.getOptions().colors[0],
            yAxis: 1,
            data: (function() {
                var data = [];
                <?php
                for($i = 0 ;$i<count($rawdata3);$i++){
                ?>
                    data.push([<?php echo $rawdata3[$i]["Tiempo"];?>,<?php echo $rawdata3[$i]["Vbat"];?>]);
                <?php } ?>
              return data;
              })()
            
            },
        {      name: 'VPlaca',
            yAxis: 3,
                data: (function () {
                     var data = [];
                <?php
                for($i = 0 ;$i<count($rawdata3);$i++){
                ?>
                    data.push([<?php echo $rawdata3[$i]["Tiempo"];?>,<?php echo $rawdata3[$i]["Vplaca"];?>]);
                <?php } ?>
                    return data;
                }())
            },
            {name: 'PWM',
            yAxis: 2,
            color: Highcharts.getOptions().colors[4],
            data: (function() {
                var data = [];
                <?php
                for($i = 0 ;$i<count($rawdata3);$i++){
                ?>
                    data.push([<?php echo $rawdata3[$i]["Tiempo"];?>,<?php echo $rawdata3[$i]["PWM"];?>]);
                <?php } ?>
              return data;
              })()
            },
            
        
                ]
                                
      });
      

    function recibirDatosFV() {
      $.ajax({
        url: 'datos_fv.php',
        success: function(data) {
                        
            chart_vbat.series[0].setData([data[0][3]]);
            chart_vbat.yAxis[0].setTitle({
              text: data[0][8] - data[0][9]+ ' Wh' //Wh bateria  posi-neg
                });
            
            chart_vbat.setSubtitle({
              text: data[0][8]+'/'+ data[0][9]+ ' Wh' //Wh bateria  posi-neg
                });
                
            
            chart_soc.series[0].setData([data[0][4]]);
            //chart_soc.yAxis[0].setTitle({
              //text: data[0][16] // Mod_bat
              //text: 'Tabs='+data[0][18] +'sg - Tflot='+ data[0][19]+ 'sg' // Tabs /Tflot
              //  });
                
            chart_temp.series[0].setData([data[0][14]]); //Temp Bat
            chart_temp.series[1].setData([data[1]]);     //CPU

            chart_ibat.series[0].setData([data[0][2]]);  //Ibat o Excedentes Red
            //chart_ibat.series[1].setData([data[0][10]]); //Iplaca (no se usa en Red)
            
            chart_wplaca.series[0].setData([data[0][12]]); //Wplaca
            
            //chart_wplaca.setTitle({
            //  text: data[0][12] // ejem de cambio de titulo
            //   });
            chart_wplaca.yAxis[0].setTitle({
              text: [data[0][13]+' Wh'] // Wh_placa
                });
            
            //var consumo_wh= parseInt(data[0][13] - (data[0][8] -data[0][9]))
            //var consumo_wh= Math.round(data[0][13] - (data[0][8] -data[0][9]))
            var consumo_wh= round(data[0][13] - (data[0][8] -data[0][9]),1)
            
            chart_consumo.series[0].setData([data[0][16]]); // Consumo
            chart_consumo.series[1].setData([data[0][10]-data[0][2]]); // Iplaca - Ibat
            chart_consumo.setSubtitle({
              text: consumo_wh + ' Wh'//data[0][13]-(data[0][8] - data[0][9]))//+ " Wh"
                });
            
            
            chart_vplaca.series[0].setData([data[0][11]]); //Vplaca
            
            grafica_i.setTitle({
              text: 'Fecha: ' + data[0][1]
                });
            grafica_i.setSubtitle({
              text: 'PWM=' + data[0][15]
                });
            
            
            x = (new Date()).getTime(); // current time
            
            grafica_i.series[0].addPoint([x, data[0][2]], true, true); //Ibat
            grafica_i.series[1].addPoint([x, data[0][10]], true, true); //Iplaca
            grafica_i.series[3].addPoint([x, data[0][11]], true, true); //Vplaca
            //grafica_i.series[3].addPoint([x, data[0][6]], true, true); //Aux1
            grafica_i.series[4].addPoint([x, data[0][15]], true, true); //PWM
            grafica_i.series[2].addPoint([x, data[0][3]], true, true); //Vbat
            
            //Valores de la tabla
            $("#Wh_placa").text(data[0][13]+ " Wh");
            //$("#Wh_Cons").text((data[0][13])-(data[0][8] - data[0][9])+ " Wh");
            $("#Wh_Cons").text(consumo_wh +' Wh')
            $("#Whp_bat").text(data[0][8]+ " Wh");
            $("#Whn_bat").text(data[0][9]+ " Wh");
            $("#Mod_bat").text(data[0][17]);
            $("#minSOC").text(data[0][21] + "%");
            $("#maxSOC").text(data[0][22]+ "%");
            $("#minVbat").text(data[0][23]+ "V");
            $("#maxVbat").text(data[0][24]+ "V");
            
            //Evaluacion del color de la celda segun la variable Mod_bat, SOCmax... (Colores definidos en inicio.css)
            //MOD_BAT o INYECCCION/CONSUMO RED
            if (data[0][17] == "CONS")  {
                document.getElementById("Mod_bat").className = "rojo";}
            else if (data[0][17] == "INYEC")  {
                document.getElementById("Mod_bat").className = "verde";}
            /*
            else if (data[0][17] == "FLOT")  {
                document.getElementById("Mod_bat").className = "FLOT";}
            else if (data[0][17] == "EQU")  {
                document.getElementById("Mod_bat").className = "EQU";};
             */
              
            //SOC_min
            if (data[0][21] <= SOC_min_rojo)  {
                document.getElementById("minSOC").className = "rojo";}
            else if (data[0][21] < SOC_min_naranja)  {
                document.getElementById("minSOC").className = "naranja";}
            else  {
                document.getElementById("minSOC").className = "verde";};
             
            //SOC_max
            if (data[0][22] <= SOC_max_rojo)  {
                document.getElementById("maxSOC").className = "rojo";}
            else if (data[0][22] < SOC_max_naranja)  {
                document.getElementById("maxSOC").className = "naranja";}
            else  {
                document.getElementById("maxSOC").className = "verde";};
            
            //minVbat
            if (data[0][23] <= Vbat_min_rojo)  {
                document.getElementById("minVbat").className = "rojo";}
            else if (data[0][23] < Vbat_min_naranja)  {
                document.getElementById("minVbat").className = "naranja";}
            else  {
                document.getElementById("minVbat").className = "verde";};
            
            //maxVbat
            if (data[0][24] >= Vbat_max_alta_rojo)  {
                document.getElementById("maxVbat").className = "rojo";}
            else if (data[0][24] >= Vbat_max_alta_naranja)  {
                document.getElementById("maxVbat").className = "naranja";}
            else if (data[0][24] <= Vbat_max_baja_rojo)  {
                document.getElementById("maxVbat").className = "rojo";}
            else if (data[0][24] <= Vbat_max_baja_naranja)  {
                document.getElementById("maxVbat").className = "naranja";}
                
            else  {
                document.getElementById("maxVbat").className = "verde";};

            
            // Actualizacion Reles     
            var tCategories = [];
            chart_reles.series[0].setData(data[2]);
            
            for (i = 0; i < chart_reles.series[0].data.length; i++) {
                tCategories.push(chart_reles.series[0].data[i].name);
            }
            
            chart_reles.xAxis[0].setCategories(tCategories);
            
            
            //console.log(data)
            //console.log(data[2])
            //console.log(data[3])
            //console.log(tCategories)
            
            setTimeout(recibirDatosFV, 3000);
          },
        cache: false
      });
      }

    function round(value, precision) {
        var multiplier = Math.pow(10, precision || 0);
    return Math.round(value * multiplier) / multiplier;
    }

});

</script>
</html>