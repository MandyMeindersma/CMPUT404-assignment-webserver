#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def check_if_file_exsists(self, path, dict_of_files):
        for file in dict_of_files.values():
            for item in file:
                if path == item:
                    f = open("./www"+item, "r")
                    return f.read()
        for file in dict_of_files.values():
            for item in file:
                if path+"index.html" == item:
                    f = open("./www"+item, "r")
                    return f.read()
        return False

    def get_all_files(self):
        dict_of_files = {}
        dict_of_files['./www/'] = []
        for filename1 in os.listdir('./www/'):
            if filename1.endswith(".css") or filename1.endswith(".html"):
                dict_of_files['./www/'].append(os.path.join('/', filename1))
            else:
                for filename2 in os.listdir('./www/'+filename1+"/"):
                    if filename2.endswith(".css") or filename2.endswith(".html"):
                        try:
                            dict_of_files['./www/'+filename1+"/"].append(os.path.join('/'+filename1+'/', filename2))
                        except:
                            dict_of_files['./www/'+filename1+"/"] = [os.path.join('/'+filename1+'/', filename2)]
                    else:
                        pass
        return dict_of_files

    def get_return_string(self, data_type, path, dict_of_files):
        if data_type == 'GET':
            file_exsist = self.check_if_file_exsists(path, dict_of_files)
            if not file_exsist:
                    resp = "HTTP/1.1 404 Not Found\r\n\r\n"
                    return resp
            else:
                if path.endswith('.css'):
                    resp = "HTTP/1.1 200 OK \r\nContent-Type: text/css;\r\n\r\n"+file_exsist
                    return resp
                else:
                    resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html;\r\n\r\n"+file_exsist
                    return resp
        else:
            resp = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            return resp

    def handle(self):
        self.all_files = self.get_all_files()
        self.data = self.request.recv(1024).strip()

        data_split = self.data.split()
        # get requests type
        self.data_type = data_split[0].decode('utf-8')
        #get path
        self.path = data_split[1].decode('utf-8')
        self.resp = self.get_return_string(self.data_type, self.path, self.all_files)



        #print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray(self.resp,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
