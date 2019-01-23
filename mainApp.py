import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QListWidgetItem 
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QInputDialog, QPlainTextEdit, QLabel, QFileDialog

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
import os
from main import EmailInfo, readSetting

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 100
        self.top = 100
        self.width = 720
        self.height = 480
        self.initUI()
 
    def addSender(self):
        row = self.senderList.currentRow()
        text, ok = QInputDialog.getText(self, "Địa chỉ thư gửi", "Gõ địa chỉ thư người gửi")

        if ok and text is not None:
            self.senderList.insertItem(row, text)

    def editSender(self):
        row = self.senderList.currentRow()
        item = self.senderList.item(row)

        if item is not None:
            text, ok = QInputDialog.getText(self, "Địa chỉ thư gửi", "Sửa địa chỉ thư người gửi", 
                QLineEdit.Normal, item.text())
            if ok and text is not None:
                item.setText(text)
    def deleteSender(self):
        row = self.senderList.currentRow()
        item = self.senderList.item(row)

        if item is not None:
            reply = QMessageBox.question(self, "Xoá thư", "Bạn có chắc muốn xoá địa chỉ " + str(item.text()),
                QMessageBox.Yes | QMessageBox.No )
            
            if reply == QMessageBox.Yes:
                item = self.senderList.takeItem(row)
                del item

    def loadFromObject(self, emails):
        row = self.senderList.currentRow()

        self.senderList.addItems([email.sender for email in emails])

        if len(emails) > 0:
            self.titleTextbox.setText(emails[0].title)
            self.contentTextBox.setPlainText(emails[0].content)
            self.recipientTextbox.setText(emails[0].to)


    def selectFile(self):
        # filePath = QFileDialog(self)
        filePath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        print (filePath)
        if os.path.isfile(filePath):

            self.attachLabel.setText(os.path.basename(filePath))
            row = self.fileListWidget.currentRow()
        
            self.fileListWidget.insertItem(row, os.path.basename(filePath))
            self.attachments[os.path.basename(filePath)] = filePath

    def deleteFile(self):
        row = self.fileListWidget.currentRow()
        item = self.fileListWidget.item(row)

        if item is not None:
            reply = QMessageBox.question(self, "Xoá thư", "Bạn có chắc muốn xoá địa chỉ " + str(item.text()),
                QMessageBox.Yes | QMessageBox.No )
            
            if reply == QMessageBox.Yes:
                item = self.fileListWidget.takeItem(row)
                self.attachments.pop(item.text(), None)
                del item
            
    def loadData(self):
        filePath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        emails = readSetting(filePath)

        self.loadFromObject(emails)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        
 
        # Create a button in the window
        self.loadSettingBtn = QPushButton('Load data', self)
        self.loadSettingBtn.move(20,80)
        self.loadSettingBtn.clicked.connect(self.loadData)

        self.addButton = QPushButton("Thêm thư", self)
        self.addButton.move(20, 110)
        self.addButton.clicked.connect(self.addSender)

        self.editButton = QPushButton("Sửa thư", self)
        self.editButton.move(20, 140)
        self.editButton.clicked.connect(self.editSender)

        self.delButton = QPushButton("Xoá thư", self)
        self.delButton.move(20, 170)
        self.delButton.clicked.connect(self.deleteSender)


        # File label 
        self.attachLabel = QLabel(self)
        self.attachLabel.setText("File")
        self.attachLabel.move(20, 210)
        self.attachLabel.resize(80, 20)


        self.addFileButton = QPushButton("Them file dinh kem", self)
        self.addFileButton.move(100, 210)
        self.addFileButton.clicked.connect(self.selectFile)

        self.delFileButton = QPushButton("Xoa file dinh kem", self)
        self.delFileButton.move(100, 240)
        self.delFileButton.clicked.connect(self.deleteFile)

        self.fileListWidget = QListWidget(self)
        self.fileListWidget.move(20, 270)

        self.fileListWidget.show()
        self.attachments = {}

        # Create sender list
        self.senderList = QListWidget(self)
        self.senderList.move(320, 20)
        self.senderList.show()

        # create to edit line
        # create Title edit line
        self.titleTextbox = QLineEdit(self)
        self.titleTextbox.move(20, 20)
        self.titleTextbox.resize(280,20)


        # create recipient
        self.recipientTextbox = QLineEdit(self)
        self.recipientTextbox.move(20, 50)
        self.recipientTextbox.resize(280,20)
        # create content text box

        self.contentTextBox = QPlainTextEdit(self)
        self.contentTextBox.move(320, 240)
        self.contentTextBox.resize(280, 200)

        # attachment label name

 
        # connect button to function on_click
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())