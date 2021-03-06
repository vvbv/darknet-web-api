# Darknet Web API
Api REST para el uso de darknet en reconocimiento de imágenes desde otras aplicaciones. Esta api retorna un JSON como respuesta, con las posibilidades y su porcentaje de probabilidad de los objetos que hay en la imagen.

<b> Testeado en GNU/Linux Debian 8.5 con python 2.7</b>

# Uso
1. Ubicar darknet-web-api.py en la misma carpeta de darknet.
2. Correr darknet-web-api.py (Por defecto el puerto es 8085).

## Ejemplos
<code>python darknet-web-api.py 8080</code>  
<code>Corriendo en 127.0.0.1:8080</code>  

<code>python darknet-web-api.py</code>  
<code>Corriendo en 127.0.0.1:8085</code>  

# Prueba

Se puede abrir en el navegador la dirección http://localhost:8085
y hacer la prueba asistida, o se puede usar curl como se muestra
a continuación

<code>curl -X POST -F file=@archivo.jpg http://localhost:8085</code>

Las predicciones junto con las salidas, quedan almacenadas en la carpeta de predicciones.

# Repositorio de darknet
Proyecto original: [<a target="_blank" href="https://github.com/pjreddie/darknet">Darknet</a>] <b>-</b> 
Port de windows: [<a target="_blank"  href="https://github.com/AlexeyAB/darknet">Darknet</a>]

### Compilación de darknet en GNU/Linux - CPU
1. <code>git clone https://github.com/pjreddie/darknet.git</code>
2. <code>cd darknet</code>
3. <code>make -j numero_de_cores_+_1</code> <b>ej: (make -j 7 para un pc con 6 cores)</b>

### Compilación de darknet en GNU/Linux - GPU
Para este procedimiento, hay que tener instalado [<a  target="_blank" href="https://developer.nvidia.com/cuda-downloads">CUDA</a>].

1. <code>git clone https://github.com/pjreddie/darknet.git</code>
2. <code>cd darknet</code>
3. Modificar el archivo Makefile y en la primer linea poner <b>GPU=1</b>
4. <code>make -j numero_de_cores_+_1</code> <b>ej: (make -j 7 para un pc con 6 cores)</b>

### Compilación de darknet en Windows
1. Guia del port [<a  target="_blank" href="https://github.com/AlexeyAB/darknet#how-to-compile-on-windows">aquí</a>]

