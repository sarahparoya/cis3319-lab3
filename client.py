import socket
from des import DesKey


def client_program():
    host = socket.gethostname()
    port = 12345  # socket server port number

    # create the socket in the client side
    s = socket.socket()
    s.connect((host, port))  # connect to the server
    desFile = open("deskey.txt", "r")
    hmacFile = open("hmackey.txt", "r")

    desKeystr = desFile.read()
    key = DesKey(desKeystr.encode('utf-8'))  # create a key
    message = input(" -> ")

    while message.lower().strip() != 'bye':
        ct = key.encrypt(message.encode('utf-8'), padding=True)
        print("shared DES key: %s"%desKeystr)
        print("sent plaintext: %s" % message)
        print("sent ciphertext: %s" % ct.decode('utf-8', 'ignore'))
        print("===========================================================")
        s.send(ct)

        data = s.recv(1024)  # receive response
        print("received ciphertext: %s" % data.decode('utf-8', 'ignore'))
        pt = key.decrypt(data, padding=True).decode()
        print("received plaintext: %s" % pt)
        print("===========================================================")

        message = input(" -> ")  # again take input
    s.close()  # close the connection
    desFile.close()
    hmacFile.close()


if __name__ == '__main__':
    client_program()
