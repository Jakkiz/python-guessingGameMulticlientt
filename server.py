import random
import socket

def generateRandomNumber():
    number = random.randint(1, 30)
    #print("Generated random number : " + str(number))
    return number

def checkIfClose(randomNumber, numberGuessed):
    n = 3
    if (numberGuessed <= (randomNumber + n))and(numberGuessed >= (randomNumber-n)):
        message = "Close\r\n"
    else :
        message = "Far\r\n"
    return message

def whatIsYourGuess(randomNumber, numberGuessed):
    while True:
        try: 
            if randomNumber != numberGuessed:
                message = checkIfClose(randomNumber, numberGuessed)
            else:
                message = "Correct\r\n"
            break
        except ValueError:
            print("Make sure u enter a number")
    return message
    
def returnNumberFromString(string):
    number = ""
    symbol = " "
    counter = 13
    lenght = len(string)
    while counter < lenght:
        number = number + string[counter]
        counter = counter + 1
    intNumber = int(number)
    #print(str(intNumber))
    return intNumber

#MAIN ######################

host = "localhost"
port = 4000

server_address = (host, port)
s = socket.socket()
s.bind(server_address)
#player dictionary addr
player = {}
mGreetings = "Greetings\r\n"
mReady = "Ready\r\n"
disconnected = False

s.listen(1)

while True:
    #print("Waiting for connections")
    c, addr = s.accept()
    #print("Connection from : " + str(addr))
    while True:
        try:
            data = c.recv(1024)
        except:
            print("Client disconnected")
        else:
            message = str(data.decode())
            if message == "Hello\r\n":
                try:
                    #print(message)
                    c.send(mGreetings.encode())
                except:
                    print("Client Disconnected")
                    disconnected = True;
                else:
                    break
    while True:
        try:
            data = c.recv(1024)
        except:
            print("Client disconnected")
        else:
            message = str(data.decode())
            if message == "Game\r\n":
                try:
                    #print(message)
                    c.send(mReady.encode())
                except:
                    print("Client Disconnected")
                    disconnected = True;
                else:
                    break

    if not disconnected:
        randomNumber = generateRandomNumber()
        player[str(addr)] = randomNumber
        while True:
            try:
                data = c.recv(1024)
                randomNumber = player[str(c.getpeername())]
            except:
                print("Client Error")
                break
            else:
                #print ("from client user: " + str(data.decode()))
                #decode
                numberGuessed = returnNumberFromString(str(data.decode()))
                message = whatIsYourGuess(randomNumber, numberGuessed)
                #print ("sending: " + message)
                c.send(message.encode())
                if message == "Correct\r\n":
                    gameRunning = 1
                    break
    else:
        c.close()


