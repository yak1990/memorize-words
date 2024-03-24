import sys
from PySide2.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSplitter, 
    QFileDialog
)
from PySide2.QtCore import Qt







class MyView(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 400)  # 增加窗口大小以便更清晰地查看布局

        self.splitter = QSplitter(Qt.Horizontal)  # 创建一个水平分割器

        # 左侧布局和小部件
        left_widget = QWidget()
        self.left_layout = QVBoxLayout(left_widget)

        # 添加按钮
        self.add_button = QPushButton('添加条目')
        self.add_button.clicked.connect(self.add_item)
        self.left_layout.addWidget(self.add_button)

        # 右侧布局和小部件
        right_widget = QWidget()
        self.text_layout = QHBoxLayout(right_widget)
        self.word_label = QLabel('', right_widget)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setWordWrap(True)
        self.text_layout.addWidget(self.word_label)

        # 将左侧和右侧小部件添加到分割器中
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(right_widget)
        self.splitter.setStretchFactor(0, 1)  # 设置左侧小部件的初始比例因子
        self.splitter.setStretchFactor(1, 3)  # 设置右侧小部件的初始比例因子

        # 设置中央小部件
        self.setCentralWidget(self.splitter)

    def set_mousePressEvent(self, func):
        self.mousePressEvent = func


    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 打开文件选择对话框
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            return file_name
        return None


    def add_item(self):
        item_layout = QHBoxLayout()
        label = QLabel(f'条目 {self.left_layout.count()}')
        delete_button = QPushButton('删除')
        delete_button.clicked.connect(lambda: self.remove_item(item_layout))

        item_layout.addWidget(label)
        item_layout.addWidget(delete_button)

        # 创建一个小部件用于存放条目布局，并将其添加到左侧布局中
        item_widget = QWidget()
        item_widget.setLayout(item_layout)
        self.left_layout.addWidget(item_widget)

    def remove_item(self, item_layout):
        # 获取条目布局所在的小部件并从左侧布局中移除
        item_widget = item_layout.parentWidget()
        if item_widget:
            item_widget.deleteLater()

    def set_text(self, now_text):
        self.word_label.setText(now_text)

    def resizeEvent(self, event):
        new_font_size = max(8, min(self.width() // 40, self.height() // 20))
        font = self.word_label.font()
        font.setPointSize(new_font_size)
        self.word_label.setFont(font)
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MyView("使用QSplitter设置左右比例")
    view.set_text("拖动中间的分割线来调整左右布局的比例。")
    view.show()
    sys.exit(app.exec_())
