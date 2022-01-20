import math
import random
import socket
import sys
import os
import struct
from PyQt5.QtWidgets import QApplication, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 1025

file = ""
file_size = 0


def upld():
    try:
        # connecting to server
        soc.connect((ip, port))
        log.append("Connection successful\n")
    except:
        status.setText("Connection unsuccessful.")
        return
    try:
        file = onChanged()
        # check file
        content = open(file, "rb")
    except IOError as e:
        print(e)
        status.setText("Couldn't open file.")
        return
    try:
        # send upload req
        soc.send(str.encode("UPLD"))
    except Exception as e:
        print(e)
        status.setText("Couldn't make server request")
        return
    try:
        # Wait for server acknowledgement then send file details
        # Wait for server ok
        log.append("Sending File details...\n")
        a =soc.recv(1024)
        print(a.decode())
        # Send file name size and file name
        soc.send(struct.pack("h", sys.getsizeof(file)))
        soc.send(str.encode(file))
        # Wait for server ok then send file size
        a = soc.recv(1024)
        print(a.decode())
        soc.send(struct.pack("i", os.path.getsize(file)))
    except:
        status.setText("Error sending file details")
        return

    try:
        # Send the file in chunks defined by 1024
        # Doing it this way allows for unlimited potential file sizes to be sent
        log.append("Sending file...\n")
        l = content.read(1024)
        counter = int.from_bytes(l, "big")
        size =os.path.getsize(file)
        while l:
            soc.send(l)
            l = content.read(1024)
            counter += int.from_bytes(l, "big")
            print(counter)
        content.close()
        status.setText("File Delivered")
        log.append("File Delivered\n")
    except Exception as e:
        status.setText("Error sending file")
        print(e)
        return
    return


def disconnect():
    soc.send(str.encode("QUIT"))
    soc.recv(1024)
    soc.close()
    status.setText("Server connection ended")
    log.append("Connection closed !\n")
    return


def onChanged():
    txt = qbox.currentText()
    f = {
        "File 1": "C:\\Users\\Sepehr\\PycharmProjects\\CN2Project\\Client\\1.txt",
        "File 2": "C:\\Users\\Sepehr\\PycharmProjects\\CN2Project\\Client\\2.txt",
        "File 3": "C:\\Users\\Sepehr\\PycharmProjects\\CN2Project\\Client\\3.txt",
        "File 4": "C:\\Users\\Sepehr\\PycharmProjects\\CN2Project\\Client\\4.txt",
        "File 5": "C:\\Users\\Sepehr\\PycharmProjects\\CN2Project\\Client\\5.txt",
    }

    return f.get(txt)


app = QApplication(sys.argv)
window = QWidget()
window.resize(300, 300)
window.setWindowTitle("Client")
dlgLayout = QVBoxLayout()
layout = QFormLayout()

qbox = QComboBox()
qbox.addItems(["File 1", "File 2", "File 3", "File 4", "File 5"])
layout.addRow("Choose File :", qbox)
status = QLineEdit()
status.setReadOnly(True)
layout.addRow("Status :", status)
log = QTextEdit()
log.setReadOnly(True)
layout.addRow("Log :", log)
dlgLayout.addLayout(layout)

btn = QPushButton("Upload")
btn.clicked.connect(upld)
dlgLayout.addWidget(btn)

qbtn = QPushButton("Quit")
qbtn.clicked.connect(disconnect)
dlgLayout.addWidget(qbtn)

window.setLayout(dlgLayout)
window.show()
sys.exit(app.exec_())
