import sys
from PySide2.QtWidgets import QApplication
import view
import control
import model
import my_event
import pickle
import os

def save_squeeze(data,data_path):
        with open(data_path, 'wb') as f:
            pickle.dump(data, f)



def main():
    app = QApplication(sys.argv)
    dispatcher=my_event.EventDispatcher()

    cache_path=r'db.cache'
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            my_model = pickle.load(f)
    else:
        my_model = model.MyModel()
        save_squeeze(my_model,cache_path)

    def update_cache(event_data):
         type_list=[
              my_event.WordEventType.to_known,
              my_event.ButtonEvnetType.add_file,
              my_event.ButtonEvnetType.remove_file,
         ]
         now_data=event_data.data
         if 'type' in now_data:
              now_type=now_data['type']
              if now_type in type_list:
                   save_squeeze(my_model,cache_path)
    
    dispatcher.add_listener(my_event.EvnetType.mouse,update_cache)
    dispatcher.add_listener(my_event.EvnetType.button,update_cache)



    my_view = view.MyView(r'单词本',dispatcher)
    my_controller = control.MyController(my_model, my_view,dispatcher)
    my_view.show()
    app.exec_()

if __name__ == "__main__":
    main()