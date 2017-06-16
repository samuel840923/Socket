# Samuel Chen, Yuning Wu, Min Cheng
#Group 22

# Import socket module
import threading
from socket import *
from threading import Thread
from time import sleep


def client():
    # This command
    player_c = player
    name = ''
    global players
    global playername
    global clientthread
    play = 0
    my_g = 0

    while True:
        if play == 0:
            sentence = player_c.recv (1024).decode ()
        if sentence == 'st':
            sleep (45)
            print ('......')
        line = sentence.split (' ')
        if line[0] == 'login' and line[1] not in playername:
            players.append (player_c)
            playername.append (str (line[1]))
            name = str (line[1])
            player_c.send ('ok'.encode ())
            continue
        if line[0] == 'who':
            kk = 'who ' + " ".join (playername)
            print (kk)
            player_c.send (kk.encode ())
            continue
        if line[0] == 'games':
            print ('games now :', pig)
            player_c.send ('game'.encode ())
            kk = ','.join (pig)
            if kk == '':
                kk = 'empty'
            player_c.send (kk.encode ())
        if line[0] == 'exit':
            playername.pop (playername.index (name))
            player_c.send ('bye'.encode ())
            return
        if line[0] == 'play':
            if line[1] in playername and line[1] not in playing:
                player_c.send ('1'.encode ())
                players[playername.index (line[1])].send ('2'.encode ())
                print ('i sent 2 to ', players[playername.index (line[1])])
                global player11
                player11 = player_c
                global player22
                player22 = players[playername.index (line[1])]
                turn = 1
                game = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
                player1 = player11
                player2 = player22
                global gameId
                gameId += 1
                my_g = gameId - 1
                temp = []
                temp.append (str (gameId))
                temp.append (name)
                temp.append (playername[playername.index (line[1])])
                tempS = ' '.join (temp)
                pig.append (tempS)
                # newthread = threading.Thread(target=playgame)
                # newthread.start()
                # threads.append(newthread)
                # newthread.join()
                play = 1
            else:
                player_c.send ('fail'.encode ())
        if play == 1:
            sentence = ''
            sentence2 = ''
            if turn == 1:
                sentence1 = player1.recv (1024).decode ()
                line1 = sentence1.split (' ')
            elif turn == 2:
                sentence2 = player2.recv (1024).decode ()
                print (sentence2)
                line2 = sentence2.split (' ')

            if sentence1 == "over" or sentence2 == 'over':
                print ('overla1')
                game = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
                turn = 1
                play = 0
                gameId -= 1
                pig.pop(my_g)
                my_g = 0
                continue

            if (line1[0]) == 'place' and turn == 1:
                if game[int(line1[1]) - 1] == '0':
                    game[int(line1[1]) - 1] = '1'
                    kk = "".join(game)
                    print(kk)
                    player1.send(kk.encode())
                    player2.send(kk.encode())
                    turn = 2
                    print('Player 1 Placed: ', line1[1])
                else:
                    player1.send('fail'.encode())
            elif (line2[0]) == 'place' and turn == 2:
                if game[int(line2[1]) - 1] == '0':
                    game[int(line2[1]) - 1] = '2'
                    kk = "".join(game)
                    print(game)
                    player1.send(kk.encode())
                    player2.send(kk.encode())
                    turn = 1
                    print('Player 2 Placed: ', line2[1])
                else:
                    print(turn)
                    player2.send('fail'.encode ())


# Prepares server socket to listen for incoming connections
serverPort = 7789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# Establishes server connection
print('The server is ready to receive')
threads = []
playing = []
gameId = 0
pig = []

players = []
playername = []
player11 = ''
player22 = ''
clientthread = []
flag = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Keep connection to server
while True:
    player, addr = serverSocket.accept ()
    newthread = Thread(target=client)
    newthread.start()
    clientthread.append(newthread)
    flag.append(1)



    # while True:
    #     if (turn==-1):
    #         sentence1 = player1.recv(1024).decode()
    #         line1 = sentence1.split(' ')
    #         sentence2 = player2.recv(1024).decode()
    #         line2 = sentence2.split(' ')
    #     elif (turn == 1):
    #         sentence1 = player1.recv(1024).decode()
    #         line1 = sentence1.split(' ')
    #     elif (turn == 2):
    #         sentence2 = player2.recv(1024).decode()
    #         line2 = sentence2.split(' ')
    #
    #     if line1[0]=='login':
    #         username1 = line1[1]
    #         print('User1 : ',username1)
    #     if line2[0]=='login':
    #         username2 = line2[1]
    #         print('User2 : ',username2)
    #
    #     if sentence1=="over" or sentence2 == "over":
    #         print('overla')
    #         game = ['0','0','0','0','0','0','0','0','0']
    #         sentence2 = ''
    #         sentence1 = ''
    #         turn = 1;
    #         continue;
    #
    #     if turn==-1:
    #         player1.send('Success 1'.encode())
    #         player2.send('Success 2'.encode())
    #         turn = 1
    #
    #     if (line1[0])=='place' and turn == 1:
    #         if game[int(line1[1])-1]=='0':
    #             game[int(line1[1])-1] = '1'
    #             kk = "".join(game)
    #             print(game)
    #             player1.send(kk.encode())
    #             player2.send(kk.encode())
    #             turn = 2
    #             print('Player 1 Placed: ',line1[1])
    #         else:
    #             player1.send('fail'.encode())
    #     elif (line2[0])=='place' and turn == 2:
    #         if game[int(line2[1])-1]=='0':
    #             game[int(line2[1])-1] = '2'
    #             kk = "".join(game)
    #             print(game)
    #             player1.send(kk.encode())
    #             player2.send(kk.encode())
    #             turn = 1
    #             print('Player 2 Placed: ',line2[1])
    #         else:
    #             player2.send('fail'.encode())
