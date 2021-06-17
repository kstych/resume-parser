import ast
import sys
import json
import time
import spacy

from urllib.parse import unquote
from http.server import BaseHTTPRequestHandler, HTTPServer

nlp = spacy.load("en_core_web_sm")

hostName = ""
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        doc = nlp(unquote(self.path)[1:])

        tokens=[]
        for token in doc:
          head=token.head
          headstr='{"i":'+str(head.i)+',"ent_type":'+str(head.ent_type)+',"ent_type_":"'+head.ent_type_+'","ent_iob":'+str(head.ent_iob)+',"ent_iob_":"'+head.ent_iob_+'","ent_id":'+str(head.ent_id)+',"ent_id_":"'+head.ent_id_+'","text":"'+head.text.replace("\"", "\\\"")+'","pos":"'+head.pos_+'","dep":'+str(head.dep)+',"dep_":"'+head.dep_+'"}'

          tokens.append('{"i":'+str(token.i)+',"ent_type":'+str(token.ent_type)+',"ent_type_":"'+token.ent_type_+'","ent_iob":'+str(token.ent_iob)+',"ent_iob_":"'+token.ent_iob_+'","ent_id":'+str(token.ent_id)+',"ent_id_":"'+token.ent_id_+'","text":"'+token.text.replace("\"", "\\\"")+'","pos":"'+token.pos_+'","dep":'+str(token.dep)+',"dep_":"'+token.dep_+'","head":'+headstr+'}')

        self.wfile.write(bytes('{"doc":'+json.dumps(ast.literal_eval(str(doc.to_json())))+',"tokens":'+'['+','.join(tokens)+']'+'}', "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
