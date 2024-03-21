
import PyPDF2
import re

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




def get_pdf_word_list(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    en_text = extract_english_and_spaces(extracted_text)
    word_list=en_text.split()
    word_list=list(set(word_list))
    return word_list



