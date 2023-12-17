#!/usr/bin/env python
# coding: utf-8

# # 라이브러리 호출

# In[31]:


get_ipython().system('pip install selenium')
get_ipython().system('pip install stylecloud')
get_ipython().system('pip install youtube_transcript_api')
get_ipython().system('pip install tqdm')


# In[1]:


## 댓글 & 제목/URL
import matplotlib.pyplot as plt
from konlpy.tag import Hannanum
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
# Expected chromedriver.exe

import tqdm
import random


# In[2]:


## 자막
from youtube_transcript_api import YouTubeTranscriptApi


# # 함수 정의

# In[3]:


# 이모티콘 제거
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

# 분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,"\n\r#\ufeff\u200d]')


# In[4]:


def get_comment(url, num_scroll = 50):
    #num_scroll = int(input('input num of scroll (50 recommend) : '))
    browser = Chrome()
    browser.get(url)
    browser.implicitly_wait(2)
    body = browser.find_element_by_tag_name('body')
    yt_id = []
    yt_content = []
    yt_likes = []
    while num_scroll:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
        num_scroll -= 1
    html0 = browser.page_source
    html = BeautifulSoup(html0, 'html.parser')
    browser.close()
    result = html.find_all("div", id='main')
    for i in result:
        i = BeautifulSoup(str(i), 'html.parser')
        try:
            yt_id.append(i.find('a', id='author-text').text)
            yt_content.append(i.find('div', id='comment-content').text)
            yt_likes.append(i.find('span', id='vote-count-middle').text)
        except:
            print('Exception!!!!!!!!!')
    df = pd.DataFrame({'id': yt_id, 'content': yt_content, 'likes': yt_likes})
    df.index = df.index.map(str)
    
    return df

def preprocess_text(text):
    text = emoji_pattern.sub('', text)
    text = han.sub('', text)
    return text

def preprocess_likes(like):
    number_like = ''.join(filter(str.isdigit, like))
    return int(number_like)

def get_id(url):
    video_id = re.search(r"v=([A-Za-z0-9_-]+)", url).group(1)
    return video_id

def comment_cleaner(text):
    return re.sub(r'간략히자세히 보기', '', text)


# In[21]:


df.head()


# # 제목 및 URL 

# In[286]:


url = 'https://www.youtube.com/@TheoBaker./videos'


# In[287]:


browser = Chrome()
browser.get(url)
browser.maximize_window()


# In[288]:


last_height = browser.execute_script("return document.getElementById('content').scrollHeight") 
while True : 
    body = browser.find_element(By.TAG_NAME,'body')
    body.send_keys(Keys.END)
    time.sleep(2.0)
    current_height = browser.execute_script("return document.getElementById('content').scrollHeight")
    if current_height == last_height :
        break 
        
    last_height = current_height
    print(last_height,current_height)
    if current_height > 20000:
        break
video_links = browser.find_elements(By.ID,'video-title-link')


# In[289]:


links = []
titles = []
for i in range(len(video_links)):
    if video_links[i].text:
        links.append(video_links[i].get_attribute('href'))
        titles.append(video_links[i].text)
    else:
        break
browser.close()


# In[290]:


data = pd.DataFrame({'title': titles, 'link': links} )


# In[291]:


data['video_num'] = data['link'].apply(get_id)
print(len(data))
data = data.sample(frac=1).reset_index(drop=True)


# In[293]:


data


# # 첫 영상관한 데이터 생성하기

# In[294]:


srt = YouTubeTranscriptApi.get_transcript(data.iloc[0,2], languages=['en'])
text = ''
for j in range(len(srt)):
    text += srt[j]['text'] + ''
df = get_comment(data.iloc[0,1],15)


# In[295]:


df['content'] = df['content'].apply(preprocess_text)
df['content'] = df['content'].apply(comment_cleaner)
df['likes'] = df['likes'].apply(preprocess_likes)


# In[296]:


df = df.sort_values('likes', ascending = False)
#df = df[df['content'].apply(lambda x: len(str(x)) > 20)].reset_index(drop = True)


# In[297]:


most_like = df.iloc[0,1]
middle_like = df.iloc[1,1]
fewest_like = df.iloc[2,1]


#while True:
 #   middle_like = df.iloc[random.randint(1, len(df) - 2), 1]
  #  if len(middle_like) > 30:
   #     break


df_partial = pd.DataFrame({'title':[data.iloc[0,0], data.iloc[0,0], data.iloc[0,0]],
                           'subtitle': [text, text, text],
                          'comment': [most_like, middle_like, fewest_like]})


# In[298]:


df_partial


# # 나머지 영상 크롤링후 concat

# In[300]:


for i in tqdm.tqdm(range(13,52)):
    #자막 추출
    srt = YouTubeTranscriptApi.get_transcript(data.iloc[i,2], languages=['en'])
    text = ''
    for j in range(len(srt)):
        text += srt[j]['text'] + ''
    # 댓글 추출
    df = get_comment(data.iloc[i,1],10)
    df['content'] = df['content'].apply(preprocess_text)
    df['content'] = df['content'].apply(comment_cleaner)
    df['likes'] = df['likes'].apply(preprocess_likes)
    
    df = df.sort_values('likes', ascending = False)
    df = df[df['content'].apply(lambda x: len(str(x)) > 20)].reset_index(drop = True)
    
    most_like = df.iloc[0,1]
    middle_like = df.iloc[random.randint(2,len(df)-2),1]
    fewest_like = df.iloc[-1,1]
    
    
    print(len(most_like), len(middle_like), len(fewest_like))
    
        
        
    df_partial_new = pd.DataFrame({'title':[data.iloc[i,0], data.iloc[i,0], data.iloc[i,0]],
                                   'subtitle': [text, text, text],
                          'comment': [most_like, middle_like, fewest_like]})
    df_partial = pd.concat([df_partial, df_partial_new])
    if len(df_partial) == 150:
        break


# In[303]:


df_partial


# In[304]:


df_partial.to_excel('NLP_theobaker.xlsx', index=False)

