#import socket module
from socket import *

#prepares server socket object
serverPort = 7789
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

#Establishes server connection
print('The server is ready to receive')
game = ['0','0','0','0','0','0','0','0','0']
turn = -1
player1, addr = serverSocket.accept()
player2, addr = serverSocket.accept()

#  keep connection to server
while True:
    # checks for a connection to the server and determines player 1 and player 2
    if (turn==-1):
        sentence1 = player1.recv(1024).decode()  # decodes message being sent
        line1 = sentence1.split(' ')
        sentence2 = player2.recv(1024).decode()
        line2 = sentence2.split(' ')
    elif (turn == 1):
        sentence1 = player1.recv(1024).decode()
        line1 = sentence1.split(' ')
    elif (turn == 2):
        sentence2 = player2.recv(1024).decode()
        line2 = sentence2.split(' ')

    # Sets username for player 1 and player 2
    if line1[0]=='login':
        username1 = line1[1]
        print('Player 1 : ',username1)
    if line2[0]=='login':
        username2 = line2[1]
        print('Player 2 : ',username2)

    # Client sends "over" when a player has lost or won
    # Starts new game automatically
    if sentence1=="over" or sentence2 == "over":
        print('Game end.')
        game = ['0','0','0','0','0','0','0','0','0']
        sentence2 = ''
        sentence1 = ''
        turn = 1;
        continue;

    if turn == -1:
        player1.send('Success 1'.encode())
        player2.send('Success 2'.encode())
        turn = 1

    if (line1[0]) == 'place' and turn == 1:
        if game[int(line1[1])-1] == '0':
            game[int(line1[1])-1] = '1'
            kk = "".join(game)
            print(game)
            player1.send(kk.encode())
            player2.send(kk.encode())
            turn = 2
            print('Player 1 Placed: ',line1[1])
        else:
            player1.send('fail'.encode())
    elif (line2[0])=='place' and turn == 2:
        if game[int(line2[1])-1]=='0':
            game[int(line2[1])-1] = '2'
            kk = "".join(game)
            print(game)
            player1.send(kk.encode())
            player2.send(kk.encode())
            turn = 1
            print('Player 2 Placed: ',line2[1])
        else:
            player2.send('fail'.encode())
