from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from shutil import copyfile

import cgi
import os
import json
import urlparse
import sys

class StoreHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        if not os.path.exists("predicciones"):
            os.makedirs("predicciones")

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        filename = form['file'].filename
        data = form['file'].file.read()

        if filename == "":
            return self.do_GET()

        open("/tmp/%s"%filename, "wb").write(data)
        copyfile("/tmp/" + filename, "uploads/" + filename)
        os.system("./darknet detect cfg/yolo.cfg  yolo.weights uploads/"+ filename +" > predicciones/salida-"+ filename +".txt")
        salida_yolo = open("predicciones/salida-"+ filename +".txt","r")
        salida_yolo = salida_yolo.read()
        
        if salida_yolo == "":
            self.respond(json.dumps({'error':'nada_identificado'}))
        else:
            posPredicted = salida_yolo.find("Predicted in") + 13
            endPredicted = salida_yolo.find("seconds")
            tiempo = salida_yolo[posPredicted:endPredicted - 1]
            predicciones_tmp = salida_yolo[endPredicted + 8:len(salida_yolo)]
            predicciones_tmp = predicciones_tmp.replace(": ",":")
            predicciones_tmp = predicciones_tmp.replace("%","")
            predicciones = predicciones_tmp.split()
            predicciones_formateadas = dict()
            contador = 0
            for prediccion in predicciones:
                tmp = prediccion.split(':')
                dict_tmp = {
                    'prediccion':tmp[0],
                    'porcentaje':tmp[1],
                }
                dict_tmp_identificado = {
                    contador : dict_tmp,
                }
                predicciones_formateadas.update(dict_tmp_identificado)
                contador = contador + 1

            retorno = {
                'tiempo_prediciendo' : tiempo,
                'predicciones' : predicciones_formateadas,
                'archivo' : filename,
            }      
            response = json.dumps(retorno)
            self.respond(response)
            filename = filename.replace('.','-')
            copyfile("predictions.png", "predicciones/prediccion-" + filename + ".png")

    def do_GET(self):
        response = """
        <html>
            <head>
                <style>
                    body{
                        color: #0ff;
                        background-color: #000011;
                    }
                    form{
                        padding: 10px 10px 10px 10px;
                        width: 40%;
                        margin-left: auto;
                        margin-right: auto;
                        margin-top: 5%;
                    }
                    .btn{
                        padding: 7px;
                        border:1px solid #0ff;
                        color: #0ff;
                        border-radius: 0px;
                        font-size: 1em;
                        background-color: transparent;
                    }
                    .btn:hover{
                        color:#FFF;
                        background-color: transparent;
                        cursor:pointer;
                        border-color: #0cc;
                        color: #0cc;
                    }
                    .file{
                        border: 1px solid #000011;
                        border-radius: 3px;
                        padding: 5px;
                    }
                    .img-darknet{
                        width: 50%;
                        border-radius:5px;
                        padding: 10px;
                    }
                    hr{
                        border-color: #bff;
                    }
                    a{
                        cursor: pointer;
                    }
                    h3{
                        color: #bff;
                    }
                </style>
            </head>
            <body>
                <a href="https://github.com/vvbv/darknet-web-api"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://camo.githubusercontent.com/38ef81f8aca64bb9a64448d0d70f1308ef5341ab/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6461726b626c75655f3132313632312e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png"></a>
                <form enctype="multipart/form-data" method="post">
                    <div><center><img class="img-darknet" src="https://pjreddie.com/static/img/darknet.png" /></center></div>
                    <p><center><h3>Darknet YOLO web API</h3></center></p>
                    <hr>
                    <p><center>Archivo(JPG): <input type="file" class="file" name="file"></center></p>
                    <hr>
                    <p><center><input type="submit" class="btn" value="Cargar"></center></p>
                </form>
            </body>
        </html>
        """        
        parsed_path = urlparse.urlparse(self.path)
        #print parsed_path
        self.respond(response)

    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)  

def iniciarServidor(puerto):
    server = HTTPServer(('', puerto), StoreHandler)
    print "Corriendo en: 127.0.0.1:" + str(puerto)
    server.serve_forever()

def main():
    if len(sys.argv) == 2: 
      iniciarServidor(int(sys.argv[1]))
    else:
        iniciarServidor(8085)

if __name__ == "__main__":
    main()