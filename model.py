import csv
import random
import pdf
import word_dict

class MyModel:
    def __init__(self,pdf_path) -> None:
         w_dict=word_dict.WordModel()
         w_list=pdf.get_pdf_word_list(pdf_path)
         self.data=w_dict.get_data(w_list)
         self.now_id=int(random.uniform(0,len(self.data)))
    
    def to_next(self):
         next_id=int(random.uniform(0,len(self.data)))
         run_count=10
         while next_id==self.now_id and run_count>0:
            run_count-=1
            next_id=int(random.uniform(0,len(self.data)))
         self.now_id=next_id

    def __get_data__(self,key_name):
         return self.data[self.now_id][key_name]
    
    def get_cn(self):
         return self.__get_data__('cn')
    
    
    def get_en(self):
         return self.__get_data__('en')
        
