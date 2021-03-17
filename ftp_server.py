#ftp-server by Steve Villarreal & Corey Rice
import socket
import os
# This file must run first.
host = socket.gethostname()
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(host)
print("Waiting to connect...")
s.bind((host, port))
s.listen()
hostaddr, port = s.accept()
print("Server is running and connected!")

def listF(connection):
    # getcwd() returns the Current Working Directory.
    dir = os.getcwd()
    filesInDir = os.listdir(dir)
    returnVal = "\n".join(filesInDir)
    connection.sendall(returnVal.encode())

def retrieve(connection, fileName):
    sizeOfFile = os.path.getsize("./" + fileName)
    # send filesize across so receiver knows how big it is.
    connection.sendall(str(sizeOfFile).encode())
    # As the file exists, open it up, load it into data and send it
    file = open(fileName, 'rb')

    # easy way to set both Data and line to collect the correct encoded bytes
    Line = file.read(1024)
    Data = Line
    while(Line):
        Line = file.read(1024)
        Data += Line
    connection.sendall(Data)
    file.close()

def store(connection, fileName, fileSize):
    file = open(fileName, "wb")
    data = connection.recv(int(fileSize), socket.MSG_WAITALL)
    file.write(data) 
    
    # this gives us hella problems...
    # connection.sendall("File was stored on Server".encode())
    print("File was stored on server.")
    file.close()

# 'with' is used to close up the program after the inside block is completed.
with hostaddr: 
    while True :
        inputString = hostaddr.recv(1024).decode()
        print("Input from client received as: ", inputString)
        # Split inputString so we can access different parts of the command
        inputString = inputString.split(" ")
        if inputString[0] == '':
            continue

        if inputString[0] == "QUIT":
            print("Session is ending!")
            hostaddr.close()
            s.close()
            break

        elif inputString[0] == "LIST":
            listF(hostaddr)

        elif inputString[0] == "RETRIEVE":
                retrieve(hostaddr, inputString[1])   

        elif inputString[0] == "STORE":
                store(hostaddr, inputString[1], inputString[2])

    