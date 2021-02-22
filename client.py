import socket
import hmac
from des import DesKey


def client_program():
    host = socket.gethostname()
    port = 12345  # socket server port number


    # create the socket in the client side
    c = socket.socket()
    c.connect((host, port))  # connect to the server

    # print("Hi server, this is client.")

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        c.send(message.encode())  # send message
        data = c.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    c.close()  # close the connection


if __name__ == '__main__':
    client_program()
