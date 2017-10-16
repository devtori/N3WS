import sys
import sqlite3
from konlpy.tag import Twitter
import math
import numpy as np
from collections import Counter
from django.db.models import Q

t = Twitter()


import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), 'test'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test.settings')
django.setup()

from app.models import *
from . import zmycode



def search_cache_db(keyword) :
    cache_keyword_list = []
    cache_keywords = Cache.objects.all().values('word')
    for cache in cache_keywords:
        cache_keyword_list.append(cache['word'])
    cache_keyword_list = list(set(cache_keyword_list))


    if keyword not in cache_keyword_list:
        url_list = []
        content_list = []
        summary_list = []

        news_cache = News.objects.all().filter(Q(keyword1 = keyword) | Q(keyword2 = keyword) | Q(keyword3 = keyword)).values('url', 'content').order_by('-id')[:20]

        for news in news_cache:
            url_list.append(news['url'])
            content_list.append(news['content'])

        for i in range(len(content_list)) :
            period = content_list[i].count(".")
            ellipsis= content_list[i].count("...")
            quotation= content_list[i].count(".\"")

            sentence_number = period-ellipsis*3-quotation

            if sentence_number ==1 :
                summary_list.append(content_list[i])
                summary_list.append("")
                summary_list.append("")
            elif sentence_number ==2 :
                split_article = content_list[i].split(".")
                summary_list.append(str(split_article[0]))
                summary_list.append(str(split_article[1]))
                summary_list.append("")
            else :
                summary_list = summarize_article(content_list)


        # save keyword, summarized 3 setence in Cache.table db
        save_db(keyword, url_list, summary_list)


def summarize_article(content_list) :
    document_list = zmycode.text2pos(content_list) # input 5 articles list
    tag = zmycode.hashtag(document_list)
    sentence_list = zmycode.key_sentences(content_list, tag)
    return sentence_list


def save_db(keyword, url_list,summary_list):
    num = 0
    for i in range(len(url_list)) :
        # save url, 3 summary sentences to Cache.table db
        cache = Cache()
        cache.word = keyword
        cache.url = url_list[i]
        cache.sentence1 = summary_list[3*i]
        cache.sentence2 = summary_list[3*i+1]
        cache.sentence3 = summary_list[3*i+2]
        num = num+1
        cache.num = num
        cache.save()


#######################################################################################


# main func
def main(keyword): # 원하는 키워드 선택 = keyword
    search_cache_db(keyword)


if __name__ == '__main__':
    main()
