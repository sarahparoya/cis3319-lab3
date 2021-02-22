import socket
from des import DesKey


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 12345

    s = socket.socket()
    s.bind((host, port))
    desFile = open("deskey.txt", "r")
    hmacFile = open("hmackey.txt", "r")

    desKeystr = desFile.read()
    desKey = DesKey(desKeystr.encode('utf-8'))
    print("Connecting to client...")

    # configure how many client the server can listen simultaneously
    s.listen(10)
    connection, address = s.accept()  # accepts the new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = connection.recv(1024)
        if not data:
            break
        print("received cipher text: %s" %data.decode('utf-8', 'ignore'))
        pt = desKey.decrypt(data, padding=True).decode()
        print("received plaintext: %s" %pt)
        print("===========================================================")
        data = input(' -> ')
        ct = desKey.encrypt(data.encode('utf-8'), padding=True)
        print("shared DES key: ", desKeystr)
        print("sent plaintext: %s" % data)
        print("sent ciphertext: %s" % ct.decode('utf-8', 'ignore'))
        print("===========================================================")
        connection.send(ct)
    connection.close()
    desFile.close()
    hmacFile.close()


if __name__ == '__main__':
    server_program()
