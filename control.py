from PySide2.QtCore import Qt

class MyController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.set_mousePressEvent(self.mousePressEvent)
        self.current_word = self.model.get_en()  
        self.translation = ''  
        self.set_view()

    def set_view(self):
        now_text=f"{self.current_word}\n{self.translation}"
        self.view.set_text(now_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.translation = self.model.get_cn()
        elif event.button() == Qt.MiddleButton:
            # self.model.next()
            # self.current_word = self.model.get_en()  
            # self.translation = ''  
            pass
        elif event.button() == Qt.RightButton:
            if self.translation:
                self.model.to_next()
                self.current_word = self.model.get_en()  
                self.translation = ''  
        
        self.set_view()
