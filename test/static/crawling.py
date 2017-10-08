import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote

# URL = URL_BEFORE_PAGE_NUM + list + URL_AFTER_PAGE_NUM
URL_BEFORE_PAGE_NUM = "http://news.donga.com/List?p="  # list = (PAGE_NUM-1)*20 + 1
URL_AFTER_PAGE_NUM = '&prod=news&ymd=&m=NP'


# get article href from news list
def get_link_from_news_title(page_num, URL, output_file):
    for i in range(page_num):
        current_page_num = 1 + i*20
        position = URL.index('=')
        URL_with_page_num = URL[: position + 1] + str(current_page_num) + URL[position + 1:]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')
        for title in soup.find_all('div', 'rightList'):
            title_link = title.select('a')
            article_URL = title_link[0]['href']
            get_text(article_URL, output_file)


# crawling news test
def get_text(URL, output_file):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
        output_file.write(string_item)


# main func
def main():
    page_num = 25  # 받아올때 str형 정수형으로 변환해서 사용
    output_file_name = 'new.txt'
    URL = URL_BEFORE_PAGE_NUM + URL_AFTER_PAGE_NUM
    output_file = open(output_file_name, 'w')
    get_link_from_news_title(page_num, URL, output_file)
    output_file.close()


if __name__ == '__main__':
    main(sys.argv)
