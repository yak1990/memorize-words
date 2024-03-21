import csv
import random


class WordModel:
    def __init__(self,db_path=r'dict_data/EnWords.csv') -> None:
        self.data=[]
        with open(db_path, newline='',encoding='UTF-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for i in reader:
                    self.data.append({
                         'en':i['word'],
                         'cn':i['translation']
                    })
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
        





if __name__ == "__main__":
     a=WordModel()
     for i in a.data:
          print(i)