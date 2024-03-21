import csv
import random


class WordModel:
    def __init__(self,db_path=r'dict_data/EnWords.csv') -> None:
        self.data={}
        with open(db_path, newline='',encoding='UTF-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for i in reader:
                    self.data[i['word']]={
                         'en':i['word'],
                         'cn':i['translation']
                    }

    
    def get_data(self,data_list):
         out=[self.data[i] for i in data_list if i in self.data]
         return out
        





if __name__ == "__main__":
     a=WordModel()
     for i in a.data:
          print(i)