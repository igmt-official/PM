import sys
import json
import string
import random

# PyQt5 Class
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit



# Load Ui
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        loadUi("ui.ui", self)

        self.generateButton.clicked.connect(self.randomPassword)
        self.saveButton.clicked.connect(self.save)
        self.searchButton.clicked.connect(self.search)
        self.passwordEchoType.clicked.connect(self.passwordEcho)

        self.show()

    # Search
    def search(self):
        web = self.webLine.text()

        if web == "":
            self.alert("warning", "Please fill out the website field.")
            return

        try:
            with open("./data.json", "r") as data:
                data_file = json.load(data)
        except FileNotFoundError:
            self.alert("warning", "No data found.")
        else:
            if web not in data_file:
                self.alert("warning", f"{web} is not exist.")
            else:
                self.emailLine.setText(data_file[web]["email"])
                self.passwordLine.setText(data_file[web]["password"])

    # Generate Random Password
    def randomPassword(self):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        sym = string.punctuation

        length = 8
        temp = lower + upper + num + sym

        random_password = random.sample(temp, length)
        password = "".join(random_password)

        self.passwordLine.setText(password)

    # Save
    def save(self):
        web = self.webLine.text()
        email = self.emailLine.text()
        password = self.passwordLine.text()

        if web == "" or email == "" or password == "":
            self.alert("warning", "Please fill out the blank.")
            return

        # Json Data
        new_data = {web: {"email": email, "password": password}}

        try:
            with open("./data.json", "r") as data:
                data_file = json.load(data)
        except FileNotFoundError:
            with open("./data.json", "w") as data:
                json.dump(new_data, data, indent=4)
                self.alert("success", f"{web} successfully added.")
        else:
            if web not in data_file:
                self.alert("success", f"{web} successfully added.")
            else:
                if password not in data_file[web]["password"] and email not in data_file[web]["email"]:
                    self.alert("success", f"{web} successfully update.")
                elif password not in data_file[web]["password"]:
                    self.alert("success", "Password successfully update.")
                elif email not in data_file[web]["email"]:
                    self.alert("success", "Email successfully update.")

            data_file.update(new_data)
            with open("./data.json", "w") as data:
                json.dump(data_file, data, indent=4)
        finally:
            self.webLine.clear()
            self.passwordLine.clear()

    # Echo Mode
    def passwordEcho(self):
        if self.passwordLine.echoMode() == QLineEdit.Password:
            self.passwordLine.setEchoMode(QLineEdit.Normal)
            self.passwordEchoType.setIcon(QtGui.QIcon("img/show.png"))
        else:
            self.passwordLine.setEchoMode(QLineEdit.Password)
            self.passwordEchoType.setIcon(QtGui.QIcon("img/hidden.png"))

    # Alert
    def alert(self, type, message):
        if type == "warning":
            self.pmAlert.setStyleSheet("color: rgb(255, 70, 70);")
            self.pmAlert.setText(message)
        elif type == "success":
            self.pmAlert.setStyleSheet("color: rgb(85, 255, 127);")
            self.pmAlert.setText(message)


app = QApplication(sys.argv)
ui = Ui()
ui.setFixedSize(570, 420)
sys.exit(app.exec_())
