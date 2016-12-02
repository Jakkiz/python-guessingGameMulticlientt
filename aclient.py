import socket
import pickle

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
port = 4001
server_address = (host, port)
s = socket.socket()
aClientRunning = 0;
connected = False

mHello = "Hello\r\n"
mGame = "Who\r\n"

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
        if message == "Admin-Greetings\r\n":
            try:
                #print(message)
                s.send(mGame.encode())
            except:
                #print("Server Disconnected")
                connected = False
                s.close()
                break
            else:
                break

if connected == True:
    while aClientRunning == 0:
        message = str(input("Enter 'Who' to get the player IPs: "))
        #message = "Who"
        while True:
            try:
                s.send(str(message + "\r\n").encode())
            except:
                #print("Server busy")
                s.close()
                aClientRunning = 1
                break
            else:
                break
        if aClientRunning == 0:
            try:
                print("The players currently playing are: ")
                data = s.recv(1024)
                message = str(data.decode())
                newMess = message.split("\n")
                print(newMess)
                if newMess[0] == '22':
                    print("There are not active player")
                else:
                #print("message received")
                print(message)
                break;
            except:
                print("error")
            
        else:
            s.close()
            break



