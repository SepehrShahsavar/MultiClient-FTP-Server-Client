import socket
import sys
import os
import struct
import struct
from _thread import *
from PyQt5.QtWidgets import QApplication, QLineEdit, QLabel
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 1025
soc.bind((ip, port))
soc.listen(5)


def upload(conn):
    # Send message once server is ready to recieve file details
    conn.send(str.encode("1"))
    # Get file detail
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length)
    file_name = file_name.decode().replace("Client", "Server")
    print(file_name)
    print(file_name_length)
    # Send message to let client know server is ready for document content
    conn.send(str.encode("1"))
    # Receive file size
    file_size = struct.unpack("i", conn.recv(4))[0]
    # Initialise and enter loop to receive file content
    try:
        output_file = open(file_name, "wb")
    except IOError as e:
        print(e)
    # This keeps track of how many bytes we have recieved, so we know when to stop the loop
    bytes_received = 0
    print("Receiving...\n")
    while bytes_received < file_size:
        l = conn.recv(1024)
        output_file.write(l)
        bytes_received += 1024
    output_file.close()
    print("Received File : {}".format(file_name))
    return


def disconncet(conn, threadCounter):
    conn.send(str.encode("1"))
    conn.close()
    print("Connection with Client " + str(threadCounter) + " closed!")
    threadCounter - 1


def threadConnection(conn, addr):
    while True:
            b = conn.recv(1024)
            data = b.decode()
            if data == "UPLD":
                upload(conn)
            if data == "QUIT":
                disconncet(conn, threadCounter)
                break


threadCounter = 0
print("Server up ... !")
while True:

    conn, addr = soc.accept()
    start_new_thread(threadConnection, (conn, addr))
    threadCounter += 1
    print("Client number " + str(threadCounter) + " is connected\n")

soc.close()
print("Server is shutting down ... !")
os.execl(sys.executable, sys.executable, *sys.argv)
