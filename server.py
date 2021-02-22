import socket
from des import DesKey
import hmac


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 12345  # initiate port number above 1024

    s = socket.socket()  # creating socket object

    # binding the host address and port together
    s.bind((host, port))
    print("Connecting to client...")

    # configure how many client the server can listen simultaneously
    s.listen(10)
    connection, address = s.accept()  # accepts the new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = connection.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        connection.send(data.encode())  # send data to the client

    connection.close()  # close the connection


if __name__ == '__main__':
    server_program()
