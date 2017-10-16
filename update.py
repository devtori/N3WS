import sys
from bs4 import BeautifulSoup
import urllib.request
from konlpy.tag import Twitter
from collections import Counter
import sqlite3
import time
from urllib.request import HTTPError

import os
import sys
import django


sys.path.append(os.path.join(os.path.dirname(__file__), 'test'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test.settings')
django.setup()

from app.models import *



t = Twitter()
# URL = URL_BEFORE_PAGE_NUM + list + URL_AFTER_PAGE_NUM
URL_BEFORE_PAGE_NUM = "http://news.donga.com/List?p="  # list = (PAGE_NUM-1)*20 + 1
URL_AFTER_PAGE_NUM = '&prod=news&ymd=&m=NP'


# get article href from news list
def get_link_from_news_title(page_num, URL, result_list, url_list):
    for i in range(page_num):
        current_page_num = 1 + (page_num-1-i) * 20
        position = URL.index('=')
        URL_with_page_num = URL[: position + 1] + str(current_page_num) \
                            + URL[position + 1:]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')
        for title in soup.find_all('div', 'rightList'):
            title_link = title.select('a')
            article_URL = title_link[0]['href']

            if article_URL not in url_list :
                Cache.objects.all().delete()
                get_text(article_URL, result_list)



# crawling news test
def get_text(URL, result_list):
    try :
        source_code_from_url = urllib.request.urlopen(URL)

    # handle if news been deleted
    except HTTPError as e:
        print(URL,"404 Page NotFound")

    # if news exist
    else :
        soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
        content_of_article = soup.select('div.article_txt')
        whole_article = ''


        # make article simple
        for item in content_of_article:
            string_item = item.find_all(text=True)

            try:
                string_item.remove('\n')
                string_item.remove( '\n')
            except :
                pass

            string_item[0]=string_item[0]+"."

            real_content_num = 0
            remove_string = ""
            for i in range(0,len(string_item)) :
                if "추천해요" in string_item[i] :
                    real_content_num+= i
                if "©" in string_item[i] :
                    remove_string=string_item[i]
                    real_content_num-= 1

            try :
                string_item.remove(remove_string)
            except :
                pass

            if real_content_num!=0 :
                whole_article = " ".join(string_item[:real_content_num -1])
                whole_article = whole_article.replace("\n","")
                whole_article = whole_article.replace("\r","")
            else :
                whole_article=""


            whole_article = " ".join(string_item[:real_content_num -1])
            whole_article = whole_article.replace("\n","")
            whole_article = whole_article.replace("\r","")


        # make article exception > photo news
        if whole_article:
            if "크게보기" not in whole_article:
                if len(whole_article) > 100:
                    result_list.append(URL)
                    result_list.append(whole_article)
                    keyword(whole_article, result_list)
        result_list.clear()


def keyword(article_text, result_list):
    replace_dic = {'추천': '', '베스트': '', '기사': '', '칼럼': '', '동아': '', '직후': '', '올해': '', '때문': '', '관련': '', '대한': '',
                   '따위': '', '따름': '', '나위': '', '대로': ''
        , '만큼': '', '마리': '', '가마': '', '묶음': '', '바리': '', '오늘': '', '내일': '', '듯이': '', '종류': '', '테야': '', '사람': '',
                   '그릇': '', '덩어리': '', '발자국': ''
        , '군데': '', '채로': '', '이것': '', '저것': '', '그루': '', '무엇': '', '우리': '', '누구': '', '너희': '', '어디': '', '언제': '',
                   '통해': '', '이하': '', '이상': ''
        , '위한': '', '일부': '', '해당': '', '다음': '', '이전': '', '경우': '', '최후': '', '기자': '', '등등': '', '켤레': '', '자루': '',
                   '미터': '', '마일': ''
        , '센치': '', '센티': '', '킬로미터': '', '등지': '', '내지': '', '위해': '', '위하여': '', '대해': '', '에서': '', '가장': '',
                   '최근': '', '라며': '', '정도': ''
        , '다른': '', '같은': '', '지금': '', '현재': '', '당시': '', '동안': '', '다시': '', '처음': '', '단지': '', '크게': '', '작게': '',
                   '가운데': '', '보기': '', '모든': ''
        , '물론': '', '실제': '', '주요': '', '대부분': '', '비롯': '', '비록': '', '여기': '', '저기': '', '한편': '', '그동안': '',
                   '지난': '', '특별': '', '아직': '', '바로': ''
        , '또한': '', '중이': '', '중인': '', '다만': '', '본격': '', '적극': '', '까지': '', '더욱': '', '얘기': '', '로부터': '', '주변': '',
                   '년대': '', '내부': '', '인근': ''
        , '향후': '', '먼저': '', '해도': '', '그대로': '', '별로': '', '이제': '', '여부': '', '매우': '', '아주': '', '모두': '', '넉달': '',
                   '이번': ''}

    def swap(document, dic):
        for Xword in document:
            if len(Xword) == 1:  # 단어의 길이가 1일 경우
                index = document.index(Xword)
                document[index] = document[index].replace(Xword, '')  # 단어삭제
            elif Xword in dic:  # 그외의 경우
                index = document.index(Xword)
                document[index] = document[index].replace(Xword, dic[Xword])  # 대체가능한 단어 적어놓은 것 중에서 실행
        return document

    # token

    def text2pos(silsigan):
        contentPos = []
        word_tag_pairs = t.pos(silsigan, norm=True, stem=True)
        keywords = [word for word, tag in word_tag_pairs if tag == 'Noun']
        contentPos.extend(keywords)
        return swap(contentPos, replace_dic)

    token = text2pos(article_text)

    FreqDict = Counter(token)
    FreqDict[''] = 0  # FreqDict 안에 ''의 빈도수값을 0으로 바꿔버림
    data = FreqDict.most_common(3)

    keyword1 = data[0]
    result_list.append(keyword1[0])
    keyword2 = data[1]
    result_list.append(keyword2[0])
    keyword3 = data[2]
    result_list.append(keyword3[0])

    news = News()
    news.url = result_list[0]
    news.content = result_list[1]
    news.keyword1 = result_list[2]
    news.keyword2 = result_list[3]
    news.keyword3 = result_list[4]
    news.save()

    result_list.clear()



# main func
def main():
    while 1 :
        page_num = 10
        URL = URL_BEFORE_PAGE_NUM + URL_AFTER_PAGE_NUM
        result_list = []

        # make recent DB url_list
        url_list = []
        newses = News.objects.order_by('-id')[:200]
        url_list = [news.url for news in newses]

        get_link_from_news_title(page_num, URL, result_list, url_list)

        time.sleep(600)


if __name__ == '__main__':
    main()
