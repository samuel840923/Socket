import sys
leng = len(sys.argv)
if leng != 3:
	print("need three arg")
def printhelp():
	print ("help: this command takes no argument.")
	print ("login: this command takes one argument, your name. A player name is a userid that uniquely identifies a player")
	print ("place: this command issues a move")
	print ("exit: the player exits the server")
def printgame():
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
def win():
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
from socket import*
serverName = sys.argv[1]
portnum = sys.argv[2]
serverPort = int(portnum)
login = "login"
place = "place"
player = 0
turn = 0
count = 0
over = "over"
clientSocket = socket(AF_INET, SOCK_STREAM)
while True:
	if turn == 1:
		print("please wait for player to place the move")
		result = clientSocket.recv(1024).decode()
		print("this is the fucking" ,result);
		if result != "fail": 
			alist = list(result)
			count = count + 1
			printgame()
			check = win()
			print(check)
			turn =0
			if check==True:
				print("you lose")
				print("starting over...")
				clientSocket.send(over.encode())
				count = 0;
				if player == 0:
					turn =0
				else:
					turn =1
			elif count == 9:
				print("the game is tied")
				print("starting over...")
				clientSocket.send(over.encode())
				count =0
				if player == 0:
					turn =0
				else:
					turn =1
		else:
			print("invalid move")
	else:
		sentence = input('Enter option:')  
		if sentence == "help":
				printhelp()
		elif login in sentence:
				clientSocket.connect((serverName,serverPort))  
				clientSocket.send(sentence.encode())
				print("please wait...")
				result = clientSocket.recv(1024).decode()
				if result == "Success 2":
					player =1;
					turn =1;
		elif place in sentence:
				print(sentence);
				clientSocket.send(sentence.encode())
				result = clientSocket.recv(1024).decode()
				print(result)
				if result != "fail": 
					alist = list(result)
					count = count +1
					printgame()
					check = win()
					turn =1
					if check==True:
						print("you win")
						print("starting over...")
						clientSocket.send(over.encode())
						count =0
						if player == 0:
							turn =0;
						else:
							turn =1;
					elif count == 9: 
						print("the game is tied")
						print("starting over...")
						clientSocket.send(over.encode())
						count =0;
						if player == 0:
							turn =0;
						else:
							turn =1;
				else:
					print("invalid move")
		elif sentence == "exit":
				clientSocket.send("exit".encode())
				clientSocket.close()
				break
