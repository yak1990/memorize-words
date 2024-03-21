import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel
from PySide2.QtCore import Qt

class MyView(QMainWindow):
    def __init__(self,title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 200)


        self.word_label = QLabel('', self)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setGeometry(50, 50, 300, 100) 
    

    def set_mousePressEvent(self,func):
        self.mousePressEvent=func

    def set_text(self,now_text):
        self.word_label.setText(now_text)
