# Samuel Chen, Yuning Wu, Min Cheng
#Group 22

# ----------Tic Tac Toe Client----------
import sys
import threading
from socket import *
leng = len(sys.argv)
if leng != 3:
    print("need three arg")
def printHelp():
    # Prints list of supported commands with brief descriptions
    print("help: This command takes no argument.")
    print("login: This command takes one argument, your name. Name is a userID that uniquely identifies a player.")
    print("place: This command issues a move.")
    print("exit: The player exits the server.")
    print("games: This command triggers a query sent to the server.")
    print("who: This command has no argument. It triggers a query message that is sent to the server.")
    print("play: This command takes one argument, the name of player X you'd like to play a game with.")


def printGame(alist):
    # This command prints out the tic-tac-toe board
    for i in range(9):  # List of strings from index 0-9
        if i % 3 == 0:
            print('\n')
        if alist[i] == "1":
            print("O", end='|')
        elif alist[i] == "2":
            print("X", end='|')
        else:
            print("-", end='|')
    print('\n')


def win(alist):
    # This command determines if a player has successfully won if they get the same
    # row/column/diagonal, alist[] is the list of strings that represent the board
    if alist[0] == alist[1] == alist[2]:
        if alist[0] == "1" or alist[0] == "2":  # across the top
            return True
    if alist[3] == alist[4] == alist[5]:
        if alist[3] == "1" or alist[3] == "2":  # across the middle
            return True
    if alist[6] == alist[7] == alist[8]:
        if alist[6] == "1" or alist[6] == "2":  # across the bottom
            return True
    if alist[0] == alist[3] == alist[6]:
        if alist[0] == "1" or alist[0] == "2":  # down the left
            return True
    if alist[1] == alist[4] == alist[7]:
        if alist[1] == "1" or alist[1] == "2":  # down the middle
            return True
    if alist[2] == alist[5] == alist[8]:
        if alist[2] == "1" or alist[2] == "2":  # down the right
            return True
    if alist[0] == alist[4] == alist[8]:
        if alist[0] == "1" or alist[0] == "2":  # diagonal top left to bottom right
            return True
    if alist[2] == alist[4] == alist[6]:
        if alist[2] == "1" or alist[2] == "2":  # diagonal top right to bottom left
            return True
    return False


def printGames(ls):
    # This command determines whether or not a game is currently being played
    if ls == "empty":
        return
    if ls == "":
        return
    a = ls.split(",")
    for i in a:
        test = i.split(" ")
        print("game id:", test[0], "who:", test[1], " vs ", test[2])


def clientwait(clientSocket):
    # This command determines the winner and loser of the game
    turn = 0
    while True:
        player = 0
        count = 0
        get = clientSocket.recv(1024).decode()
        get = get.split(" ")
        if get[0] == "who":
            print(get)
        if get[0] == "bye":
            return
        elif get[0] == "game":
            ls = clientSocket.recv(1024).decode()
            print(ls)
            printGames(ls)
        elif get[0] == "2" or get[0] == "1":
            if get[0] == "2":
                clientSocket.send("st".encode())
                player = 1
            while count < 9:
                if player == 0:
                    rec = clientSocket.recv(1024).decode()
                    if rec != "fail":
                        alist = list(rec)
                        printGame(alist)
                        check = win(alist)
                        if check == True:
                            print("You win the game!")
                            clientSocket.send("over".encode())
                            player = 0
                            print("The game has ended. Please input another command, or 'exit' to leave the server.")
                            break
                        else:
                            player = 1
                            count = count + 1
                            if count == 9:
                                # If all spots are filled, the game results in a draw
                                print("Tie game. Please input another command, or 'exit' to leave the server.")
                                clientSocket.send("over".encode())
                                break
                    else:
                        print("Invalid case")
                else:
                    print ("Please wait...")
                    rec = clientSocket.recv (1024).decode ()
                    if rec != "Fail":
                        alist = list(rec)
                        printGame(alist)
                        check = win(alist)
                        if check == True:
                            print("You lose the game.")
                            clientSocket.send("over".encode())
                            print("Game has ended. Please input another command, or 'exit' to leave the server.")
                            break
                        else:
                            count = count + 1
                            if count == 9:
                                print("Tie game. Please input another command, or 'exit' to leave the server.")
                                clientSocket.send("over".encode ())
                                break
                        player = 0
                    else:
                        print("Invalid case")


# Establishes connection to server
serverName = sys.argv[1]
portnum = sys.argv[2]
serverPort = int(portnum)
login = "login"
place = "place"
log = 0
over = "over"
play = "play"
start = 0
alist = []
clientSocket = socket(AF_INET, SOCK_STREAM)
t1 = threading.Thread(target=clientwait, args=(clientSocket,))

while True:
    sentence = input('Enter option:')
    if login in sentence:
        # This command determines if the player has logged in successfully
        if log == 1:
            print ("You have already logged in.")
        else:
            # Connect to server
            clientSocket.connect ((serverName, serverPort))
            clientSocket.send (sentence.encode ())
            result = clientSocket.recv (1024).decode ()
            if result == "ok":
                print ("Login success")
                log = 1
                t1.start ()
            else:
                print ("Invalid input, please try again.")
    elif sentence == "who":
        # Allows the player to see who is connected to the server
        clientSocket.send ("who".encode())
    elif sentence == "exit":
        # Exits out of the server
        clientSocket.send("exit".encode())
        break
    elif sentence == "games":
        # Allows the player to see who is in a game
        clientSocket.send("games".encode())
    elif sentence == "help":
        # Prints out help command
        printHelp()
    elif play in sentence:
        # Allows the player to choose which other player to play a game with
        clientSocket.send(sentence.encode())
    elif place in sentence:
        # This allows the player to place their position on the Tic-Tac-Toe board
        clientSocket.send(sentence.encode())
        print(sentence)
t1.join()
