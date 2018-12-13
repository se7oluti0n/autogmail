import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QListWidgetItem 
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QInputDialog

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
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

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        
 
        # Create a button in the window
        self.button = QPushButton('Show text', self)
        self.button.move(20,80)

        self.addButton = QPushButton("Thêm thư", self)
        self.addButton.move(20, 110)
        self.addButton.clicked.connect(self.addSender)

        self.editButton = QPushButton("Sửa thư", self)
        self.editButton.move(20, 140)
        self.editButton.clicked.connect(self.editSender)

        self.delButton = QPushButton("Xoá thư", self)
        self.delButton.move(20, 170)
        self.delButton.clicked.connect(self.deleteSender)


        # Create sender list
        self.senderList = QListWidget(self)
        self.senderList.move(320, 20)
        self.senderList.addItems(["Hello", "GOodbye"])
        self.senderList.show()

        # create to edit line
        # create Title edit line
        self.titleTextbox = QLineEdit(self)
        self.titleTextbox.move(20, 20)
        self.titleTextbox.resize(280,40)
        # create content text box

        # attachment label name
 
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
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