import sys
from PySide2.QtWidgets import QApplication
import view
import control
import model

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_model = model.WordModel()
    my_view = view.MyView(r'单词本')
    my_controller = control.MyController(my_model, my_view)
    my_view.show()
    app.exec_()