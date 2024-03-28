import sys
from PySide2.QtWidgets import QApplication
import view
import control
import model
import my_event

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dispatcher=my_event.EventDispatcher()
    my_model = model.MyModel()
    my_view = view.MyView(r'单词本',dispatcher)
    my_controller = control.MyController(my_model, my_view,dispatcher)
    my_view.show()
    app.exec_()