from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from shutil import copyfile

import cgi
import os
import json

class StoreHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        filename = form['file'].filename
        data = form['file'].file.read()
        open("/tmp/%s"%filename, "wb").write(data)
        copyfile("/tmp/" + filename, "uploads/" + filename)
        os.system("./darknet detect cfg/yolo.cfg  yolo.weights uploads/"+ filename +" > salida.txt")
        salida_yolo = open("salida.txt","r")
        salida_yolo = salida_yolo.read()
        #Tempo
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

    def do_GET(self):
        response = """
        <html><body>
        <form enctype="multipart/form-data" method="post">
        <p>File: <input type="file" name="file"></p>
        <p><input type="submit" value="Upload"></p>
        </form>
        </body></html>
        """        
        self.respond(response)

    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)  

server = HTTPServer(('', 8085), StoreHandler)
server.serve_forever()