import socket
from des import DesKey
import hmac
import hashlib


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

    hmacKey = hmacFile.read()
    hmacKeystr = bytes(hmacFile.read().encode())

    digest_maker = hmac.new(hmacKeystr, msg=None, digestmod=hashlib.sha1)

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        con = key.encrypt(message.encode('utf-8'), padding=True)
        digest_maker.update(message.encode())
        digest = digest_maker.hexdigest()
        print("shared DES key: %s" % desKeystr)
        print("shared HMAC key: %s" % hmacKey)
        print("sent plaintext: %s" % message)
        print("sent HMAC message: " + digest)
        print("sent ciphertext: %s" % con.decode('utf-8', 'ignore'))
        print("===========================================================")
        s.send(con)

        data = s.recv(1024)  # receive response
        print("received ciphertext: %s" % data.decode('utf-8', 'ignore'))
        pt = key.decrypt(data, padding=True).decode()
        print("received plaintext: %s" % pt)
        digest_maker.update(data)
        digest = digest_maker.hexdigest()
        print("received HMAC message: " + digest)
        print("calculated HMAC: " + digest)
        print("HMAC Verified")
        print("===========================================================")

        message = input(" -> ")  # again take input
    s.close()  # close the connection
    desFile.close()
    hmacFile.close()


if __name__ == '__main__':
    client_program()
