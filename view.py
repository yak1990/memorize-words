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
    QTextEdit,
    QLineEdit
)
from PySide2.QtCore import Qt, QTimer
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




class WordWidget(QWidget):
    def __init__(self,dispatcher):
        super().__init__()
        self.init_ui()
        self.setFocusPolicy(Qt.StrongFocus)


        self.dispatcher=dispatcher

        self.en_text='请添加pdf'
        self.cn_text=''
        self.en_sentence=''
        self.cn_sentence=''
        self.same_en_list=[]
        self.detail_stu=False

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()

        # 创建标签和编辑框
        self.en_label = QLabel("")
        self.en_label.setWordWrap(True)

        self.cn_label = QLabel("")
        self.cn_label.setWordWrap(True)
        
        self.en_sentence_label = QLabel("")
        self.en_sentence_label.setWordWrap(True)
        
        self.cn_sentence_label = QLabel("")
        self.cn_sentence_label.setWordWrap(True)
        
        self.synonyms_label = QLabel("")
        self.synonyms_label.setWordWrap(True)
    

        # 将控件添加到布局中
        layout.addWidget(self.en_label)
        layout.addWidget(self.cn_label)
        layout.addWidget(self.en_sentence_label)
        layout.addWidget(self.cn_sentence_label)
        layout.addWidget(self.synonyms_label)

        # 设置布局
        self.setLayout(layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.detail_stu = not self.detail_stu
        elif event.button() == Qt.RightButton:
            
            event_data=my_event.Event(
                my_event.EvnetType.mouse,
                {
                    'type':my_event.WordEventType.to_next,
                }
            )
            self.dispatcher.dispatch(event_data)

        self.update_word_info()

    def keyPressEvent(self, event):

        # 按下f建表明记住单词
        if event.key()==70:
            event_data=my_event.Event(
                my_event.EvnetType.key,
                {
                    'type':my_event.WordEventType.to_known,
                    'en':self.en_text
                }
            )
            self.dispatcher.dispatch(event_data)



    def update_word_info(self):
        self.en_label.setText(self.en_text)
        if self.detail_stu:
            self.cn_label.setText(self.cn_text)
            self.en_sentence_label.setText(self.en_sentence)
            self.cn_sentence_label.setText(self.cn_sentence)
        else:
            self.cn_label.setText('')
            self.en_sentence_label.setText('')
            self.cn_sentence_label.setText('')

            

    
    def set_word_info(self, word_info):
        print(word_info)
        self.en_text=word_info['en']
        self.cn_text=word_info['cn']
        self.en_sentence=word_info['en_sentence']
        self.cn_sentence=word_info['cn_sentence']
        self.detail_stu=False
        self.update_word_info()

    def resizeEvent(self, event):
        new_font_size = max(8, min(self.width() // 40, self.height() // 20))
        font = self.en_label.font()
        font.setPointSize(new_font_size)
        self.en_label.setFont(font)
        self.cn_label.setFont(font)
        self.en_sentence_label.setFont(font)
        self.cn_sentence_label.setFont(font)
        super().resizeEvent(event)

class MyView(QMainWindow):
    def __init__(self, title,dispatcher):
        super().__init__()

        self.dispatcher=dispatcher
        
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 400)  # 增加窗口大小以便更清晰地查看布局
        
        
        main_splitter = QSplitter(Qt.Vertical)

        splitter = QSplitter(Qt.Horizontal)  # 创建一个水平分割器


        # 左侧布局和小部件
        self.left_widget = FileList(dispatcher)

        self.right_widget=WordWidget(dispatcher)

        # 将左侧和右侧小部件添加到分割器中
        splitter.addWidget(self.left_widget)
        splitter.addWidget(self.right_widget)
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

        # 创建一个 QTimer 实例
        self.timer = QTimer(self)
        # 设置定时器超时（触发）间隔（毫秒）
        self.timer.setInterval(1000)  # 1000 毫秒（1 秒）
        # 将定时器的 timeout 信号连接到槽函数
        self.timer.timeout.connect(self.SetUpdate)
        # 启动定时器
        self.timer.start()


    def SetUpdate(self):
        event_data=my_event.Event(
                my_event.EvnetType.update,
                None
            )
        self.dispatcher.dispatch(event_data)


    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 打开文件选择对话框
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            return file_name
        return None


    def update_word_info(self):
        self.right_widget.update_word_info()

    def set_word_info(self, word_info):
        self.right_widget.set_word_info(word_info)

    def set_file_info(self,file_data_list):
        self.left_widget.setItem(file_data_list)



    def addLog(self,message):
        """向日志框中添加一条新消息"""
        # self.logBox.append(message)  # append方法自动换行
        self.logBox.setText(message)
