import os
import sys
import json
import string
import random

# PyQt5 Classes
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget


# Load Ui
class Ui(QMainWindow):
        def __init__(self):
                super(Ui, self).__init__()
                loadUi("ui.ui", self)

                # Button
                self.generateButton.clicked.connect(self.generateRandomPassword)
                self.saveButton.clicked.connect(self.save)
                self.searchButton.clicked.connect(self.search)

                self.show()

        # Password Generator Button
        def generateRandomPassword(self):
                lower = string.ascii_lowercase
                upper = string.ascii_uppercase
                numbers = string.digits
                symbols = string.punctuation

                length = 8
                temp = lower + upper + numbers + symbols

                random_password = random.sample(temp, length)
                password = "".join(random_password)

                self.passwordLine.setText(password)

                # Debug
                # print(data.password)
                # print(password)

        # Save Button
        def save(self):
                web = self.websiteLine.text()
                email = self.emailLine.text()
                password = self.passwordLine.text()

                if web == "" or email == "" or password == "":
                        self.alert("warning", "Please fill out the blank.")
                        return

                new_data = {
                        web: {
                                "email": email,
                                "password": password
                        }
                }

                try:
                        # Append new data in json file
                        with open("./data.json", "r") as data:
                                # Reading the old data
                                data_file = json.load(data)

                except FileNotFoundError:
                        with open("./data.json", "w") as data:
                                        
                                # Saving updated data
                                json.dump(new_data, data, indent=4)

                                self.alert("success", "Data Successfully Added.")

                else:
                        if self.websiteLine.text() in data_file:
                                self.alert("success", "Password Successfully Update.")
                        else:
                                self.alert("success", "Data Successfully Added.")
                                
                        # Updating old data to new data
                        data_file.update(new_data)
                        with open("./data.json", "w") as data:

                                # Saving updated data
                                json.dump(data_file, data, indent=4)

                # No matter if succeed the try or fail, do this
                finally:
                        # Delete all value of input after adding on database
                        self.websiteLine.clear()
                        self.passwordLine.clear()      
                
        # Search Button
        def search(self):
                web = self.websiteLine.text()

                if web == "":
                        self.alert("warning", "Please fill out the website field.")
                        return

        # Alert
        def alert(self, type, message):
                if type == "warning":
                        self.alertLine.setStyleSheet("color: rgb(255, 70, 70);")
                        self.alertLine.setText(message)
                elif type == "success":
                        self.alertLine.setStyleSheet("color: rgb(85, 255, 127);")
                        self.alertLine.setText(message)


# Show Ui
app = QApplication(sys.argv)
ui = Ui()
ui.setFixedSize(570, 420)
sys.exit(app.exec_())