import socket
import sys
import threading


def readSocketAndOutput(s):
    global byeFlag
    print("Enter 'bye' to quit chat")
    while True:
        if byeFlag:
            try:
                str = s.recv(100).decode()
                print("\r>>> " + str + "\n<<<", end="", flush=True)
            except:
                print("Connection closed")
                break

            if str == "bye":
                byeFlag = 0;
                break
        
    print("Remote user disconnected!!!")
    s.close()
    sys.exit()
    
def readSTDINandWriteSocket(s):
    global byeFlag
    while True:
        if byeFlag:
            str = input("<<< ")
            s.send(str.encode())
            if str == "bye":
                print("Chat termination signal sent!!!")
                byeFlag = 0;
                s.close()
                sys.exit()
        



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
byeFlag = 1;
ch = input("Connect[1] to peer or wait[2] for peer connection. Enter choice:")

if ch == "1":
    host = input("Enter peer IP:")
    port = 54321
    s.connect((host, port))
    threading.Thread(target=readSocketAndOutput, args=(s,)).start()
    threading.Thread(target=readSTDINandWriteSocket, args=(s,)).start()
    
elif ch == "2":
    host = ''
    port = 54321
    s.bind((host, port))
    s.listen(2)              # Now wait for client connection.
    print("Waiting for connection...")
    while True:
        c, addr = s.accept()     # Establish connection with client.
        threading.Thread(target=readSocketAndOutput, args=(c,)).start()
        threading.Thread(target=readSTDINandWriteSocket, args=(c,)).start()

else:
    print("Incorrect choice")
    sys.exit()




