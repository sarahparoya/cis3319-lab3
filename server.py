import socket
from des import DesKey
import hmac
import hashlib


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

    hmacKey = hmacFile.read()
    hmacKeystr = bytes(hmacFile.read().encode())
    # byteHmacKey = bytes(hmacKeystr, encoding='utf8')
    digest_maker = hmac.new(hmacKeystr, msg=None, digestmod=hashlib.sha1)

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
        print("received cipher text: %s" % data.decode('utf-8', 'ignore'))
        pt = desKey.decrypt(data, padding=True).decode()
        print("received plaintext: %s" % pt)
        digest_maker.update(data)
        digest = digest_maker.hexdigest()

       # rhmacKey = hashlib.sha256(str(data).encode('utf-8'))

        print("received HMAC message: " + digest)
        print("calculated HMAC: " + digest)
        print("HMAC Verified")

        print("===========================================================")
        data = input(' -> ')

        ct = desKey.encrypt(data.encode('utf-8'), padding=True)
        digest_maker.update(data.encode())

        print("shared DES key: ", desKeystr)
        print("shared HMAC key: %s" % hmacKey)
        print("sent plaintext: %s" % data)
        print("sent HMAC message: " + digest_maker.hexdigest())
        print("sent ciphertext: %s" % ct.decode('utf-8', 'ignore'))
        print("===========================================================")
        connection.send(ct)
    connection.close()
    desFile.close()
    hmacFile.close()


if __name__ == '__main__':
    server_program()
