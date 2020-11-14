"""
Simple and insecure way to serve the files to external apps
"""
import http.server
import socketserver
import time
import os

PORT = 8888
SERVER ='127.0.0.1' #important to avoid exposure to internet


while True:
    try:
        os.chdir(os.path.dirname(__file__)) #change dir to real exec dir
        print ("Starting dir: ", os.getcwd())
        
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer((SERVER, PORT), Handler) as httpd:
            print("Serving at " , SERVER, "Port", PORT)
            httpd.serve_forever() # execution  stops here until it launches an exception
    except Exception as inst:
        print(type(inst))       # prints the exception instance
        time.sleep(10)          # wait 10 seconds...and retry serving ignoring the exception

#restart on error