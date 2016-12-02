import socket

def messageToPrint(string):
    if(string == "Close\r\n"):
        message = "You are close!"
    if(string == "Far\r\n"):
        message = "You are way off"
    if(string == "Correct\r\n"):
        message = "You guessed it correctly!"
    print(message)
    return

#MAIN ######################

host = "localhost"
port = 4000

server_address = (host, port)
s = socket.socket()
connected = False

mHello = "Hello\r\n"
mGame = "Game\r\n"

while True:
    try:
        s.connect(server_address)
    except:
        print("Server Not ready")
        s.close()
        break
    else:
        connected = True
        s.send(mHello.encode())
        break

while True:
    try:
        data = s.recv(1024)
    except:
        print("Server disconnected")
        s.close()
        break
    else:
        message = str(data.decode())
        if message == "Greetings\r\n":
            try:
                #print(message)
                s.send(mGame.encode())
            except:
                #print("Server Disconnected")
                s.close()
                break
            else:
                break

while True:
    try:
        data = s.recv(1024)
    except:
        #print("Server disconnected")
        s.close()
        break
    else:
        message = str(data.decode())
        if message == "Ready\r\n":
            #print(message)
            gameRunning = 0
            break

if connected == True:
    print("Welcome to the guess the number game!")
    while gameRunning == 0:
        message = str(input("What is your guess? "))
        while True:
            try:
                s.send(str("My Guess is: " + message + "\r\n").encode())
            except:
                #print("Server busy")
                s.close()
                gameRunning = 1
                break
            else:
                break
        if gameRunning == 0:            
            data = s.recv(1024)
            message = str(data.decode())
            messageToPrint(message)
            if message == "Correct\r\n":
                gameRunning = 1;
                s.close()
        else:
            break
s.close



