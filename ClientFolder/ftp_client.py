#ftp-client by Steve Villarreal & Corey Rice
import socket
import sys 
import os


class FTPConnection():
    # Constructor to set connected to false.
    def __init__(self):
        self.connected = False

    def connect(self, address, portNum):
        self.connected = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, portNum))
    
    def listF(self):
        self.sock.sendall("LIST".encode())
        print(self.sock.recv(1024).decode())
    
    def retrieve(self, fileName):
        self.sock.sendall(("RETRIEVE " + fileName).encode())

        #get filesize from server
        fileSize = self.sock.recv(1024).decode()
        file = open(fileName, "wb")
        data = self.sock.recv(int(fileSize), socket.MSG_WAITALL)
        file.write(data) 
        file.close()
        print("File Retrieved")
    
    def store(self, fileName):
        sizeOfFile = os.path.getsize("./" + fileName)
        # we tried deleting str(sizeOfFile)..... but got an error.
        self.sock.sendall(("STORE " + fileName  + " " + str(sizeOfFile)).encode())
        # 'rb' means 'read bytes'
        file = open(fileName, 'rb')

        Line = file.read(1024)
        Data = Line
        while(Line):
            Line = file.read(1024)
            Data += Line
        self.sock.sendall(Data)
        file.close()
    
    def quit(self):    
        self.sock.sendall("QUIT".encode())
        print(self.sock.recv(1024).decode())
        self.sock.close()

print("Please enter CONNECT IPADDRESS/HOSTNAME [SPACE] PORTNUM to start up the connection.")
connection = FTPConnection()
cli = "\nClientCLI> "
print("After connecting the Commands available are: \nLIST - The server will list the files in current directory" + 
"\nRETRIEVE *filename* - Allows a client to get a file specified by its file name to the server" + 
"\nSTORE *filename* - Store a file with the specified name to the server" + 
"\nQUIT - This command terminates the connection to the server \n")

while (True):
    inputs = str(input(cli))
    inputs = inputs.split(" ")
    # This puts the input to uppercase "connect" -> "CONNECT"
    inputs[0] = inputs[0].upper()

    if connection.connected == False:
        if inputs[0] == "CONNECT":
            connection.connect(inputs[1], int(inputs[2]))
            print("Connected to host: " + inputs[1] + " via portNum: " + inputs[2])
    else:
        if inputs[0] == "STORE":
                connection.store(inputs[1])
        
        elif inputs[0] == "LIST":
                connection.listF()

        elif inputs[0] == "RETRIEVE":
                connection.retrieve(inputs[1])

        elif inputs[0] == "QUIT":
            connection.quit()
            # We use this line again to free up the port.
            # It somehow works.
            connection = FTPConnection()
            break
        