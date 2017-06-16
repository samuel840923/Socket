import sys
import threading
from socket import*
leng = len(sys.argv)
if leng != 3:
	print("need three arg")
def printhelp():
	print ("help: this command takes no argument.")
	print ("login: this command takes one argument, your name. A player name is a userid that uniquely identifies a player")
	print ("place: this command issues a move")
	print ("games: this command triggers a query sent to the server")
	print ("who: this command has no argument. It triggers a query message that is sent to the server; ")
	print ("exit: the player exits the server")
	print ("play: this command takes one argument, the name of a player X you'd like to play a game with")
def printgame(alist):
	for i in range(9):
		if i%3==0:
			print('\n')
		if alist[i] == "1":
			print ("o", end = ',')
		elif alist[i] == "2":
			print ("x", end = ',')
		else:
			print ("-", end = ',')
	print('\n')
def win(alist):
	if alist[0] == alist[1] == alist[2]:
		if alist[0] == "1" or alist[0] == "2":
			return True 
	if alist[3] == alist[4] == alist[5]:
		if alist[3] == "1" or alist[3] == "2":
			return True
	if alist[6] == alist[7] == alist[8]:
		if alist[6] == "1" or alist[6] == "2":
			return True
	if alist[0] == alist[3] == alist[6]:
		if alist[0] == "1" or alist[0] == "2":
			return True
	if alist[1] == alist[4] == alist[7]:
		if alist[1] == "1" or alist[1] == "2":
			return True
	if alist[2] == alist[5] == alist[8]:
		if alist[2] == "1" or alist[2] == "2":
			return True
	if alist[0] == alist[4] == alist[8]:
		if alist[0] == "1" or alist[0] == "2":
			return True
	if alist[2] == alist[4] == alist[6]:
		if alist[2] == "1" or alist[2] == "2":
			return True
	return False
def printgames(ls):
	if ls == "empty":
		return
	if ls == "":
		return
	a = ls.split(",")
	for i in a:
		test = i.split(" ")
		print("game id :",test[0], "who: ", test[1]," vs ", test[2])
def clientwait(clientSocket):
	turn = 0
	while True:
		player = 0
		count = 0
		get = clientSocket.recv(1024).decode()
		get = get.split(" ")
		if get[0] == "who":
			print(get)
		if get[0] =="bye":
			return
		elif get[0] == "game":
			ls = clientSocket.recv(1024).decode()
			print(ls)
			printgames(ls)
		elif get[0]== "2" or get[0]== "1":
			print( "--the game has start--")
			if get[0]=="2":
				clientSocket.send("st".encode())
				player = 1
			while count < 9:
				if player == 0:
					rec = clientSocket.recv(1024).decode()
					if rec != "fail":
						print(rec)
						alist = list(rec)
						printgame(alist)
						check = win(alist)
						if check ==True:
							print ("you win the game")
							clientSocket.send("over".encode())
							player = 0
							print("is over")
							break
						else:
							player = 1
							count = count+1
							if count == 9:
								print ("tie---")
								clientSocket.send("over".encode())
								break
					else: 
						print("invalid case")
				else: 
					print("please wait")
					rec = clientSocket.recv(1024).decode()
					if rec != "fail":
						alist = list(rec)
						printgame(alist)
						check = win(alist)
						if check ==True:
							print ("you lose the game")
							clientSocket.send("over".encode())
							print("is over lose")
							break
						else: 
							count = count+1		
							if count == 9:
								print ("tie---")
								clientSocket.send("over".encode())
								break
						player = 0
					else: 
						print("invalid case")
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
t1 = threading.Thread(target=clientwait,args = (clientSocket,))
while True:
	sentence = input('Enter option:')
	if login in sentence :
		if log==1: 
			print("you already login")
		else:
			clientSocket.connect((serverName,serverPort))  
			clientSocket.send(sentence.encode())
			result = clientSocket.recv(1024).decode()
			if result == "ok":
				print("login success")
				log =1
				t1.start()
			else:
				print("not valid")
	elif sentence == "who":
		clientSocket.send("who".encode())
	elif sentence == "exit":
			clientSocket.send("exit".encode())
			break
	elif sentence == "games":
			clientSocket.send("games".encode())
	elif sentence == "help":
		printhelp()
	elif play in sentence :
		clientSocket.send(sentence.encode())
	elif place in sentence:
		clientSocket.send(sentence.encode())
		print(sentence)
t1.join()


