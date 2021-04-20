#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
import re
import datetime


# In[31]:


# df = pd.read_excel('C:/Users/jin/OneDrive/바탕 화면/키워드 2구역 복붙.xlsx')
filePath = '광뉴.xlsx'
df = pd.read_excel(filePath, engine='openpyxl')


# In[32]:


def get_region(text, text2):
    result = '알수없음'
    pattern = '((\d+-)?\d+구역)'
    try:
        return re.search(pattern, text).group(1)
    except Exception as e:
        try:
            return re.search(pattern, text2).group(1)
        except Exception as e:
            pass

    return result


# In[33]:


def get_type(text):
    result = []
    pattern = '(구역)?((\d+([abcdefghijkABCDEFGHIJK비형]|(\s?타입|\s?신청)))|(\s(59)\s|\s?(99)\s?)|(상가)\s|(17평))(신청)?'
    
    try:
        r = re.findall(pattern, text)
        for item in r:
            result.append(item[1])
    except Exception as e:
        pass
    
    return result


# In[34]:


def get_types(text, text2):
    result = get_type(text) + get_type(text2)
        
    if len(result) > 0:
        return list(set([item.replace('타입', '').strip().replace('비', 'b').replace('형', '').replace('17평', '36A').upper() for item in result]))
    return ['알수없음']
        


# In[35]:


def get_appraisal_price(text_list):
    result = '알수없음'
    pattern = '(감|김)((평가)|((정가)격?)|(정평가)|(정평가금액)|(정)|(평))?\s?;?:?\s?(\d+\,?억?\.?\s?\d+)'
    for text in text_list:
        try:
            r = re.findall(pattern, text)
            price = r[0][9].replace(',', '').replace(' ', '')
            return price
        except Exception as e:
            pass
    return result


# In[36]:


def get_primium(text_list):
    result = []
    pattern = '(피|프리미엄|p|P)\s?;?:?\s?(\d+\,?억?\.?\s?\d*천?\d*)(억)?(천)?[p\n\.만\s,추]?|(\d+)p'
    for text in text_list:
        try:
            r = re.findall(pattern, text)  
            if len(r) > 0:                
                result = result + [items[1].replace('.', '').replace(',', '').split(' ')[0] for items in r if len(items) > 0]
        except Exception as e:
            pass
        
    if len(result) > 0:
        return list(set(result))[0]
    else:
        return '알수없음'


# In[37]:


def apply_info(x):
    text, text2 = x['매물제목'], x['매물특징']
    x['구역'] = get_region(text, text2).replace('구역', '')
    x['타입'] = ','.join([str(item) for item in get_types(text, text2)])
    x['감정가'] = get_appraisal_price([text, text2])
    x['프리미엄'] = get_primium([text, text2])  
    return x


# In[38]:


df = df.apply(lambda x: apply_info(x), axis=1)


# In[39]:


df['구역'] = pd.to_numeric(df['구역'], errors='ignore')


# In[40]:


df = df.sort_values(['구역'], axis=0)


# In[41]:


df.to_excel('광뉴_{}.xlsx'.format(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')))


# In[251]:


# for text, text2 in zip(df['매물제목'], df['매물특징']):
#     print('text', text)
#     print('text2', text2)    
#     print('[지역]', get_region(text, text2)) # 구역
#     print('[타입]', get_types(text, text2)) # 타입
#     print('[감정가]', get_appraisal_price([text, text2]))
#     print('[프리미엄]', get_primium([text, text2]))
#     print('--------------------------------')  


# In[ ]:




