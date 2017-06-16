from socket import*
serverPort = 7789
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.bind(('',serverPort)) 
serverSocket.listen(2)
print('The server is ready to receive')
while True:
	connectionSocket, addr = serverSocket.accept()
	connectionSocket2, addr = serverSocket.accept()
	print(connectionSocket," this is the address ",addr)
	sentence = connectionSocket.recv(1024).decode() 
	sentence1 = connectionSocket.recv(1024).decode() 
	capitalizedSentence = sentence.upper() 
	capitalizedSentence1 = sentence1.upper() 
	connectionSocket.send(capitalizedSentence.encode())
	connectionSocket.send(capitalizedSentence1.encode())
	
