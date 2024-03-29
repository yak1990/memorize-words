
import PyPDF2
import re
import nltk
from nltk.tokenize import sent_tokenize
import os
nltk_dir='DLCache/nltk'
os.makedirs(nltk_dir,exist_ok=True)
nltk.download('punkt',download_dir=nltk_dir)

def extract_english_and_spaces(text):
    # 正则表达式仅匹配英文字符和空格
    pattern = re.compile(r'[A-Za-z ]+')
    
    # 找到所有匹配的部分
    matches = pattern.findall(text)
    
    # 将所有匹配的部分连接成一个字符串
    english_text_with_spaces = ''.join(matches)
    
    return english_text_with_spaces


def extract_text_from_pdf(pdf_path):
    # 打开PDF文件
    with open(pdf_path, 'rb') as file:
        # 创建PDF阅读器对象
        reader = PyPDF2.PdfReader(file)
        
        # 初始化一个字符串来存储全部的文字内容
        text = ''
        
        # 遍历PDF中的每一页
        for page in reader.pages:
            # 提取当前页的文字，并添加到总的文字内容中
            text += page.extract_text()
        
        return text




# def get_pdf_word_list(pdf_path):
#     extracted_text = extract_text_from_pdf(pdf_path)
#     en_text = extract_english_and_spaces(extracted_text)
#     word_list=en_text.split()
#     word_list=list(set(word_list))
#     return word_list

def robust_split_sentences(text):
        out=[]

        text=text.lower()
        # 使用换行符进行分割
        for now_text in text.split('\n'):
            # 使用 NLTK 的 sent_tokenize 进行分句
            sentences = sent_tokenize(now_text, language='english') # 如果你处理的是英文文本
            # 对于其他语言，可以更改 'language' 参数，例如 'german'、'french' 等
            sentences=[i.strip() for i in sentences]
            out.extend(sentences)
        return out

def get_pdf_word_dict(pdf_path):
    
    text=extract_text_from_pdf(pdf_path)
    sentences_list=robust_split_sentences(text)
    word_dict={}
    for id,i in enumerate(sentences_list):
         word_list=extract_english_and_spaces(i).split()
         if len(word_list):
              for now_word in word_list:
                   if now_word not in word_dict:
                        word_dict[now_word]=[]
                   word_dict[now_word].append(i)
    return word_dict
