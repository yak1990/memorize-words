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
    QListWidget, 
    QFileDialog,
    QTextEdit
)
from PySide2.QtCore import Qt
import my_event

class FileList(QWidget):
    def __init__(self,dispatcher):
        super().__init__()
        self.initUI()
        self.dispatcher=dispatcher

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.listWidget = QListWidget()

        self.addButton = QPushButton("添加pdf")
        self.removeButton = QPushButton("删除选中的pdf")

        layout.addWidget(self.listWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.removeButton)

        self.setLayout(layout)

        self.addButton.clicked.connect(self.addItem)
        self.removeButton.clicked.connect(self.removeItem)

    def setItem(self,item_name_list): 
        # 设置当前显示的项目

        self.listWidget.clear()
        self.listWidget.addItems(item_name_list)


    def addItem(self):
        event_data=my_event.Event(
                my_event.EvnetType.button,
                {
                    'type': my_event.ButtonEvnetType.add_file,
                    'stu':False
                }
            )
        
        self.dispatcher.dispatch(event_data)

    def removeItem(self):
        listItems = self.listWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            event_data=my_event.Event(
                    my_event.EvnetType.mouse,
                    {
                        'data': my_event.ButtonEvnetType.remove_file,
                        'path': item,
                        'stu':False
                    }
                )
            self.dispatcher.dispatch(event_data)


class MyView(QMainWindow):
    def __init__(self, title,dispatcher):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 400)  # 增加窗口大小以便更清晰地查看布局
        
        
        main_splitter = QSplitter(Qt.Vertical)

        splitter = QSplitter(Qt.Horizontal)  # 创建一个水平分割器

        # 左侧布局和小部件
        self.left_widget = FileList(dispatcher)

        # 右侧布局和小部件
        right_widget = QWidget()
        self.text_layout = QHBoxLayout(right_widget)
        self.word_label = QLabel('', right_widget)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setWordWrap(True)
        self.text_layout.addWidget(self.word_label)

        # 将左侧和右侧小部件添加到分割器中
        splitter.addWidget(self.left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)  # 设置左侧小部件的初始比例因子
        splitter.setStretchFactor(1, 3)  # 设置右侧小部件的初始比例因子

        
        # 创建日志框
        self.logBox = QTextEdit()
        self.logBox.setReadOnly(True)  # 设置为只读

        # 将内容分割器和日志框添加到主分割器
        main_splitter.addWidget(splitter)
        main_splitter.addWidget(self.logBox)

        # 调整分割器的分割比例
        main_splitter.setStretchFactor(0, 4)  # 上部分内容占更多空间
        main_splitter.setStretchFactor(1, 1)  # 日志框占较少空间


        # 设置中央小部件
        self.setCentralWidget(main_splitter)

        self.dispatcher=dispatcher

        self.en_text='请添加pdf'
        self.cn_text=''
        self.cn_stu=False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.cn_stu = not self.cn_stu
        elif event.button() == Qt.MiddleButton:
            event_data=my_event.Event(
                my_event.EvnetType.mouse,
                {
                    'type':my_event.WordEventType.to_known,
                    'en':self.en_text
                }
            )
            self.dispatcher.dispatch(event_data)
        elif event.button() == Qt.RightButton:
            
            event_data=my_event.Event(
                my_event.EvnetType.mouse,
                {
                    'type':my_event.WordEventType.to_next,
                }
            )
            self.dispatcher.dispatch(event_data)

        self.update_word_info()


    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 打开文件选择对话框
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            return file_name
        return None


    def update_word_info(self):
        now_str=self.en_text
        if self.cn_stu:
            now_str=f'{now_str}\n{self.cn_text}'
        self.word_label.setText(now_str)

    def set_word_info(self, en_text,cn_text):
        self.en_text=en_text
        self.cn_text=cn_text
        self.cn_stu=False
        self.update_word_info()

    def set_file_info(self,file_data_list):
        self.left_widget.setItem(file_data_list)

    def resizeEvent(self, event):
        new_font_size = max(8, min(self.width() // 40, self.height() // 20))
        font = self.word_label.font()
        font.setPointSize(new_font_size)
        self.word_label.setFont(font)
        super().resizeEvent(event)

    def addLog(self,message):
        """向日志框中添加一条新消息"""
        # self.logBox.append(message)  # append方法自动换行
        self.logBox.setText(message)
