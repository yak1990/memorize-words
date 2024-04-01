import csv
import random
import pdf

import os
import nltk
nltk_dir = 'DLCache/nltk'
os.makedirs(nltk_dir, exist_ok=True)  # 确保目录存在
nltk.data.path.append(nltk_dir)
nltk.download('wordnet', download_dir=nltk_dir)
from nltk.corpus import wordnet
from collections import defaultdict

from googletrans import Translator
import threading
import queue

import time

output_queue=queue.Queue()
input_queue = queue.Queue()
def translator_consumer(dest_language='zh-cn'):
        translator = Translator()
        while True:
            try:
               now_data = input_queue.get()
               # print(now_data)
               if now_data is None:  # 使用 None 作为生产者结束信号
                    break
               
               out_data={}
               for now_word,now_list in now_data.items():
                    print('before:',now_word)
                    translation = translator.translate(now_word, dest=dest_language)
                    out_data['en']=now_word
                    out_data['cn']=translation.text
                    out_data['sentence']=[]
                    if len(now_list)>3:
                         now_list=random.sample(now_list,3)
                    for sentence in now_list:
                         translation = translator.translate(sentence, dest=dest_language)
                         out_data['sentence'].append({
                                   'en':sentence,
                                   'cn':translation.text
                                   }
                              )
                    print('done')
                    output_queue.put(out_data)
                    print(output_queue.qsize())
                    time.sleep(0.5)
               input_queue.task_done()
            except Exception as e:
                 print(f"An error occurred: {e}")
                 time.sleep(3)
                 translator = Translator()



class MyModel:
    def __init__(self) -> None:
         self.known_words=defaultdict(list) # 已经记住的单词
         
         self.raw_word_dict=defaultdict(list)
         self.word_dict=defaultdict(list)  # 生单词
         self.pdf_words={}

         self.now_word=''
         self.now_info={}

         self.__init_view_cache__()

    
    def __init_view_cache__(self):
         self.view_cache=set()  # 当前启动浏览的单词量
         self.now_target=[]
         self.now_target_num=50
         if self.now_target_num>0 and len(self.word_dict)>self.now_target_num:
              self.now_target=random.sample(list(self.word_dict.keys()),self.now_target_num)
         else:
              self.now_target=list(self.word_dict.keys())
              
    
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['view_cache']
        del state['now_target']
        del state['now_target_num']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.__init_view_cache__()


    def add_pdf(self,pdf_path):
         w_dict=pdf.get_pdf_word_dict(pdf_path)
         w_list=[i for i in w_dict if len(wordnet.synsets(i))>0]
         w_dict={i:j for i,j in w_dict.items() if i in w_list and i not in self.known_words and i not in self.raw_word_dict}
         
         self.pdf_words[pdf_path]=[i for i in w_dict]

         
         for i,j in w_dict.items():
              self.raw_word_dict[i].extend(j)

         if self.now_word == '':
              self.to_next()

     
    def remove_pdf(self,pdf_path):
         if pdf_path not in self.pdf_words:
              return

         now_data=self.pdf_words[pdf_path]
         self.word_dict={i:j for i,j in self.word_dict.items() if i not in now_data}

         del self.pdf_words[pdf_path]
         
         self.to_next()
    
    def update(self):
         if input_queue.qsize()==0 and len(self.raw_word_dict)>0:
               input_list=[{i:j} for i,j in self.raw_word_dict.items()]
               random.shuffle(input_list)
               for i in input_list:
                    input_queue.put(i)
               input_queue.put(None)

               consumer_thread = threading.Thread(target=translator_consumer)
               consumer_thread.daemon = True
               consumer_thread.start()
               print('start translation')
         else:
               while output_queue.qsize()>0:
                    tmp_data=output_queue.get()
                    en_word=tmp_data['en']
                    self.word_dict[en_word]=tmp_data
                    del self.raw_word_dict[en_word]
                    output_queue.task_done()
         
    def to_next(self):
         w_list=[]
         if len(self.now_target)>0:
               w_list=self.now_target
         else:
               w_list=list(self.word_dict.keys())
         if len(w_list)>0:
               next_word = random.choice(w_list)
               run_count=10
               while next_word==self.now_word and run_count>0:
                    run_count-=1
                    next_word = random.choice(w_list)
               self.now_word=next_word
               
               now_sentence=random.choice(self.word_dict[self.now_word]['sentence'])
               now_info={
                    'en':self.now_word,
                    'cn':self.word_dict[self.now_word]['cn'],
                    'en_sentence':now_sentence['en'],
                    'cn_sentence':now_sentence['cn']
               }
               
               self.view_cache.add(self.now_word)
               self.now_info=now_info
         else:
              now_info={
                    'en':'暂无单词',
                    'cn':'',
                    'en_sentence':'',
                    'cn_sentence':''
               }
              if len(self.word_dict)>0 and len(self.now_target)==0:
                    now_info={
                              'en':'当前学习目标完成',
                              'cn':'',
                              'en_sentence':'',
                              'cn_sentence':''
                         }
              self.now_info=now_info
     
    def set_to_known(self,en_text):
         self.known_words[en_text].extend(self.word_dict[en_text])
         del self.word_dict[en_text]

         if en_text in self.now_target:
              self.now_target.remove(en_text)

         print(f'known len : {len(self.known_words)}')
         print(f'unfamiliar len : {len(self.word_dict)}')

     
    def set_to_unknown(self,en_text):
         self.word_dict[en_text].extend(self.known_words[en_text])
         del self.known_words[en_text]

         self.now_target.append(en_text)

         print(f'known len : {len(self.known_words)}')
         print(f'unfamiliar len : {len(self.word_dict)}')
         

    
    def get_word_info(self):
         return self.now_info
      
    
    def get_unfamiliar_size(self):
         return len(self.word_dict)
    
#     def get_known_size(self):
#          return len(self.known_words)
    
    def get_log_info(self):
         return f'this time target remain: {len(self.now_target)}, known len: {len(self.known_words)} , unfamiliar len: {len(self.word_dict)} , raw len: {len(self.raw_word_dict)} , view len: {len(self.view_cache)}'

    def get_pdf_list(self):
         out=[i for i in self.pdf_words]
         return out 

