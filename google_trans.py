'''
这是一个翻译脚本，将srt文件中的文本翻译成中文
使用googletrans库，调用google翻译的API，免费服务
https://github.com/ssut/py-googletrans
安装：
pip install googletrans
如果调用失败，尝试：
pip install googletrans==4.0.0-rc1

Basic usage:
If source language is not given, google translate attempts to detect the source language.
>>> from googletrans import Translator
>>> translator = Translator()
>>> translator.translate('안녕하세요.')
# <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
>>> translator.translate('안녕하세요.', dest='ja')
# <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
>>> translator.translate('veritas lux mea', src='la')
# <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

Attention:
The maximum character limit on a single text is 15k.

进度条：
pip install tqdm
'''

from googletrans import Translator
import re
import time
from tqdm import tqdm

# 创建翻译器实例
translator = Translator()

def safe_translate(text, src = 'auto', dest = 'zh-cn', attempts = 5):
    for attempt in range(attempts):
        try:
            return translator.translate(text, src = src, dest = dest).text
        except Exception as e:
            print(f'翻译失败，正在重试... ({attempt + 1}/{attempts})')
            if attempt < attempts - 1:
                time.sleep(2 ** attempt)
    raise Exception('翻译失败！')

def translate_srt(file_path):
    translated_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        text_to_translate = ''
        num = 1
        pbar = tqdm(desc = "Processing dynamic tasks", total = len(lines)) # 初始化进度条
        dynamic_condition = True # 动态循环条件
        iterations = 0
        
        while dynamic_condition:
            for line in lines:
                # 检查是否为需要翻译的文本行
                if not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line) and line.strip() != '':
                    text_to_translate += line.strip() + '\n'  # 收集需要翻译的文本
                    # print(num, line.strip())
                    num += 1
                else:

                    # 遇到非文本行时，翻译之前收集的文本，并添加到结果列表
                    if text_to_translate:
                        translated_text = safe_translate(text_to_translate, src='auto', dest='zh-cn')
                        # print(translated_text)
                        translated_lines.append(translated_text)
                        text_to_translate = ''  # 重置文本
                    translated_lines.append(line)  # 添加非文本行到结果列表
                    
                # 更新进度条     
                iterations += 1
                pbar.update(1)
            # 确保文件末尾的文本也被翻译
            if text_to_translate:
                translated_text = safe_translate(text_to_translate, src='auto', dest='zh-cn')
                translated_lines.append(translated_text)
            
            # 动态检查循环结束条件
            if iterations == len(lines):
                dynamic_condition = False
    
    # 保存翻译后的内容到新文件
    with open('translated.srt', 'w', encoding='utf-8') as translated_file:
        for line in translated_lines:
            translated_file.write(line)
            translated_file.write("\n")
            
# 调用函数，翻译SRT文件

def main():

    file_path = '' # 在这里填入文件路径
    print("文件路径：", file_path)
    translate_srt(file_path)
    print("翻译完成！")
    
if __name__ == '__main__':
    main()
