import ast
import sys
import json
import time
import spacy
from urllib.parse import unquote, urlsplit, parse_qs
from parser import Engine
from http.server import BaseHTTPRequestHandler, HTTPServer

en = Engine()

hostName = ""
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    
    def process_data(self, text):
        doc = en.tokeninzer(text)
        return doc
    
    def do_GET(self):
        result = {
            'status':'NO_PARAM',
            'message':'pass ?text=YOUR_DATA'
        }
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        query = parse_qs(urlsplit(self.path).query) 
        
        if 'text' in query:
            result = {
            'status':'OK',
            'response':self.process_data(''.join(query['text']))
            }   
        
        self.wfile.write(bytes(json.dumps(result), "utf-8"))
        


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
