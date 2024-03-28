from PySide2.QtCore import Qt
import my_event
import model
class MyController:
    def __init__(self, model,view,dispatch):
        self.view = view
        self.dispatch=dispatch
        self.model=model


        self.dispatch.add_listener(my_event.EvnetType.mouse,self.MouseEventHandler)
        self.dispatch.add_listener(my_event.EvnetType.button,self.ButtonEventHandler)

    
    def set_file_info(self):
        f_list=self.model.get_pdf_list()
        self.view.set_file_info(f_list)
    
    def set_word_info(self):
        self.view.set_word_info(self.model.get_en(),self.model.get_cn())

    def MouseEventHandler(self, event_data):
        event=event_data.data
        if event['type'] == my_event.WordEventType.to_known:
            en_text=event['en']
            self.model.set_to_known(en_text)
        elif event['type'] == my_event.WordEventType.to_next:
            self.model.to_next()
            self.set_word_info()
        

    
    def ButtonEventHandler(self,event_data):
        now_data=event_data.data
        if now_data['data']==my_event.ButtonEvnetType.add_file:
            now_path=self.view.get_file()
            if now_path:
                self.model.add_pdf(now_path)
        elif now_data['data']==my_event.ButtonEvnetType.remove_file:
            now_path=now_data['path']
            self.model.remove_pdf(now_path)

        self.set_file_info()
        self.set_word_info()
        