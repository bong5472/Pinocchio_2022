import requests
from bs4 import BeautifulSoup
import re

def news_crawling(url):

    headers = {'User-Agent':'Mozilla/5.0(Windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    news_article = requests.get(url,headers=headers)
    news_article_parser = BeautifulSoup(news_article.text,'html.parser',from_encoding='utf-8')
    
    # 연예뉴스 class
    if 'entertain' in url:
        class_find_title = 'end_tit'
        class_find_date = 'author'
        date_start = 5
        date_end = 15
        class_find_article = 'article_body'
    
    #일반 뉴스 class
    else:
        class_find_title = 'media_end_head_headline'
        class_find_date = '_ARTICLE_DATE_TIME'
        date_start = 1
        date_end = 11
        class_find_article = '_article_content'
    
    #뉴스 제목
    news_title_str = str(news_article_parser.find_all('h2', class_=class_find_title))
    news_title_str = re.sub('<.+?>|\n|\t', '', news_title_str, 0).strip()[1:-1]
    
    #뉴스 날짜
    news_date_str = str(news_article_parser.find_all('span', class_=class_find_date))
    news_date_str = re.sub('<.+?>', '', news_date_str, 0).strip()[date_start:date_end]

    #뉴스 본문
    news_article_str = str(news_article_parser.find_all('div', class_= class_find_article))
    news_article_str = re.sub('<.+?>|\n|\t', '', news_article_str, 0).strip()[1:-1]
    
    return news_title_str, news_article_str, news_date_str


# 본문 문장별로 분류
def article_split(news_article_str):
    split_str = news_article_str.split('.')
    raw_len = len(split_str)
    return split_str, raw_len