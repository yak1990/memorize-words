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


    def resizeEvent(self, event):
        # 调整字体大小以适应新尺寸
        new_font_size = max(10, min(self.width() // 20, self.height() // 10))  # 计算新的字体大小
        font = self.word_label.font()  # 获取当前字体
        font.setPointSize(new_font_size)  # 设置新的字体大小
        self.word_label.setFont(font)  # 应用新的字体
        super().resizeEvent(event)  # 调用父类的 resizeEvent 方法