import csv
import random
import pdf
import word_dict

class MyModel:
    def __init__(self) -> None:
         self.w_dict=word_dict.WordModel()
         self.unfamiliar_words=[] # 生单词
         self.known_words=[] # 已经记住的单词
         self.pdf_words={}
    
    def add_pdf(self,pdf_path):
         w_list=pdf.get_pdf_word_list(pdf_path)
         now_data=self.w_dict.get_data(w_list)
         now_data=[i for i in now_data if i not in self.known_words]
         
         self.pdf_words[pdf_path]=now_data

         self.unfamiliar_words.extend(now_data)
         self.unfamiliar_words=list(set(self.unfamiliar_words))

         self.now_id=int(random.uniform(0,len(self.unfamiliar_words)))

     
    def remove_pdf(self,pdf_path):
         if pdf_path not in self.pdf_words:
              return

         now_data=self.pdf_words[pdf_path]
         self.unfamiliar_words=[i for i in self.unfamiliar_words if i not in now_data]

         del self.pdf_words[pdf_path]
         
         self.to_next()

    def to_next(self):
         next_id=int(random.uniform(0,len(self.unfamiliar_words)))
         run_count=10
         while next_id==self.now_id and run_count>0:
            run_count-=1
            next_id=int(random.uniform(0,len(self.unfamiliar_words)))
         self.now_id=next_id
     
    def set_to_known(self,en_text):
         if en_text not in self.known_words:
               self.known_words.append(en_text)
         if en_text in self.unfamiliar_words:
              self.unfamiliar_words.remove(en_text)
     #     self.to_next()

         print(f'known len : {len(self.known_words)}')
         print(f'unfamiliar len : {len(self.unfamiliar_words)}')
         

    
    def get_en(self):
         return self.unfamiliar_words[self.now_id]
       
    
    def get_cn(self):
         en_text=self.get_en()
         return self.w_dict.get_cn(en_text)
      
    
    def get_unfamiliar_size(self):
         return len(self.unfamiliar_words)
    
    def get_known_size(self):
         return len(self.known_words)

    def get_pdf_list(self):
         out=[i for i in self.pdf_words]
         return out 
