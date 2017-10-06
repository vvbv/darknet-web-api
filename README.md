# Darknet Web Api
Api REST para el uso de darknet en reconocimiento de imágenes desde otras aplicaciones. Esta api retorna un JSON como respuesta, con las posibilidades y su porcentaje de probabilidad de los objetos que hay en la imagen.

<b> Testeado en GNU/Linux Debian 8.5 con python 2.7</b>

# Uso
1. Ubicar darknet-web-api.py en la misma carpeta de darknet.
2. Correr darknet-web-api.py (Por defecto el puerto es 8085).

# Prueba

Se puede abrir en el navegador la dirección http://localhost:8085
y hacer la prueba asistida, o se puede usar curl como se muestra
a continuación

<code>curl -X POST -F file=@archivo.jpg http://localhost:8085</code>

# Repositorio de darknet
Proyecto original: [<a href="https://github.com/pjreddie/darknet">Darknet</a>]
Port de windows: [<a href="https://github.com/AlexeyAB/darknet">Darknet</a>]

### Compilación en GNU/Linux - CPU
1. <code>git clone https://github.com/pjreddie/darknet.git</code>
2. <code>cd darknet</code>
3. <code>make</code>

### Compilación en GNU/Linux - GPU
Para este procedimiento, hay que tener instalado [<a href="https://developer.nvidia.com/cuda-downloads">CUDA</a>].

1. <code>git clone https://github.com/pjreddie/darknet.git</code>
2. <code>cd darknet</code>
3. Modificar el archivo Makefilem y en la primer linea poner <b>GPU=1</b>
4. <code>make</code>

### Compilación en Windows
1. Guia del port [<a href="https://github.com/AlexeyAB/darknet#how-to-compile-on-windows">aquí</a>]