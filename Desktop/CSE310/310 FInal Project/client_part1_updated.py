# Samuel Chen, Yuning Wu, Min Cheng
# CSE310 Group 22
# ----------Tic Tac Toe Client----------
import sys
# Imports socket module
from socket import *
leng = len (sys.argv)
if leng != 3:
    print("need three arg")
serverName = sys.argv[1]
portnum = sys.argv[2]
serverPort = int (portnum)
login = "login"
place = "place"
player = 0
turn = 0
count = 0
over = "over"
clientSocket = socket (AF_INET, SOCK_STREAM)
def printHelp():
    # Prints list of supported commands with brief descriptions
    print ("help: This command takes no argument.")
    print ("login: This command takes one argument, your name. Name is a userID that uniquely identifies a player.")
    print ("place: This command issues a move.")
    print ("exit: The player exits the server.")
def printGame():
    # This command prints out the tic-tac-toe board
    for i in range (9):  # List of strings from index 0-9
        if i % 3 == 0:
            print ('\n')
        if alist[i] == "1":
            print ("O", end='|')
        elif alist[i] == "2":
            print ("X", end='|')
        else:
            print ("-", end='|')
    print ('\n')
def win():
    #  This command determines if a player has successfully won
    #  if they get the same row/column/diagonal, alist is the
    #  list of strings that represent the board
    if alist[0] == alist[1] == alist[2]:  # across the top
        if alist[0] == "1" or alist[0] == "2":
            return True
    if alist[3] == alist[4] == alist[5]:  # across the middle
        if alist[3] == "1" or alist[3] == "2":
            return True
    if alist[6] == alist[7] == alist[8]:  # across the bottom
        if alist[6] == "1" or alist[6] == "2":
            return True
    if alist[0] == alist[3] == alist[6]:  # down the left
        if alist[0] == "1" or alist[0] == "2":
            return True
    if alist[1] == alist[4] == alist[7]:  # down the middle
        if alist[1] == "1" or alist[1] == "2":
            return True
    if alist[2] == alist[5] == alist[8]:  # down the right
        if alist[2] == "1" or alist[2] == "2":
            return True
    if alist[0] == alist[4] == alist[8]:  # diagonal top left to bottom right
        if alist[0] == "1" or alist[0] == "2":
            return True
    if alist[2] == alist[4] == alist[6]:  # diagonal top right to bottom left
        if alist[2] == "1" or alist[2] == "2":
            return True
    return False
while True:
    # Continues connection to server while game has not ended
    if turn == 1:
        print("Please wait for player to place the move")
        result = clientSocket.recv(1024).decode()
        if result != "fail":
            alist = list(result)
            count = count + 1
            printGame()
            check = win()
            print(check)
            turn = 0
            if check == True:
                print("You lose")
                print("Starting over...")
                clientSocket.send (over.encode ())
                count = 0;
                if player == 0:
                    turn = 0
                else:
                    turn = 1
            elif count == 9:  # All pieces on the board are filled
                print("The game is tied")
                print("Starting over...")
                clientSocket.send(over.encode ())
                count = 0
                if player == 0:
                    turn = 0
                else:
                    turn = 1
        else:
            print("Invalid move")
    else:
        sentence = input('Enter option:')
        if sentence == "help":
            printHelp()
        elif login in sentence:
            # Allows player to connect to server, waiting on other player
            clientSocket.connect((serverName, serverPort))
            clientSocket.send(sentence.encode ())
            print("please wait...")
            result = clientSocket.recv (1024).decode ()
            if result == "Success 2": # If player two connects successfully begin game
                player = 1;
                turn = 1;
        elif place in sentence:
            # Allows player to place a game piece on the Tic-Tac-Toe board
            # Determines whether or not the piece is a winning position
            print(sentence);
            clientSocket.send (sentence.encode())
            result = clientSocket.recv (1024).decode()
            print (result)
            if result != "fail":
                alist = list(result)
                count = count + 1
                printGame()
                check = win()
                turn = 1
                if check == True:
                    print("You win")
                    print("Starting over...")
                    clientSocket.send (over.encode ())
                    count = 0
                    if player == 0:
                        turn = 0;
                    else:
                        turn = 1;
                elif count == 9:
                    print("The game is tied")
                    print("Starting over...")
                    clientSocket.send (over.encode ())
                    count = 0;
                    if player == 0:
                        turn = 0;
                    else:
                        turn = 1;
            else:
                print ("Invalid move")
        elif sentence == "exit":
            # Allows player to exit out of server
            clientSocket.send("exit".encode ())
            clientSocket.close()
            break
