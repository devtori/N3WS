
########################################################################################################################
# 전처리 과정

import requests
import math
from collections import Counter

from konlpy.tag import Twitter
t = Twitter()

# 형태소 분석
useful_pos_list = ['Noun', 'Verb', 'Adjective']


same_dic = {'추천': '', '베스트': '', '기사': '', '칼럼': '', '동아': '', '직후': '', '올해': '', '때문': '', '관련': '', '대한': '',
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


def text2pos(content_list):
    contentPos = []
    for i in range(len(content_list)):
        word_tag_pairs = t.pos(content_list[i], norm=True, stem=True)
        keywords = [word for word, tag in word_tag_pairs if tag in useful_pos_list]
        contentPos.append(keywords)
    return swap(contentPos, same_dic)



def swap(content_list, dic):
    for i in range(len(content_list)):
        for word in dic:
            if word in content_list[i]:
                content_list[i] = [document.replace(word, dic[word]) for document in content_list[i]]
    return content_list


########################################################################################################################


# tf-idf 계산
def tf(word, document):
    return document.count(word) / len(document)


def n_containing(word, document_list):
    return sum(1 for document in document_list if word in document)


def idf(word, document_list):
    return math.log(len(document_list) / (1 + n_containing(word, document_list)))


def tfidf(word, document, document_list):
    return tf(word, document) * idf(word, document_list)


########################################################################################################################

# document별 키워드 생성 및 list로 저장

def hashtag(document_list):
    keyword_list = []
    for i, document in enumerate(document_list):
        # print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, document, document_list) for word in document}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        keywords = []
        for word, score in sorted_words[:5]:
            keywords.append(word)
        #    keywords.append(word)
        keyword_list.append(keywords)
    return keyword_list



########################################################################################################################


# tf-idf를 통해 추출한 키워드에 따른 중요한 문장 선별


import numpy as np
from collections import Counter


def jaccard(cent1, cent2):
    return sum((cent1 & cent2).values()) / (sum((cent1 | cent2).values())+1)

def key_sentences(document_list, tag):
    result = []
    for k in range(len(document_list)):
        temp = []
        sentences = document_list[k].replace('.  ','. ').split('. ')
        sents = text2pos(sentences)
        cents = [Counter(sent) for sent in sents]

        n = len(sents)
        A = np.zeros((n, n)) # adjacency
        M = np.zeros((n, n)) # google
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                A[i, j] = jaccard(cents[i], cents[j])

        remove_index = 0
        for i in range(n):
            if A[i].sum() == 0:
                remove_index = i+1
        if remove_index > 0 :
            del sentences[remove_index-1]

        sents = text2pos(sentences)
        cents = [Counter(sent) for sent in sents]

        n = len(sents)
        A = np.zeros((n, n)) # adjacency
        M = np.zeros((n, n)) # google
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                A[i, j] = jaccard(cents[i], cents[j])

        keys = tag[k]
        per = []

        for cent in cents:
            per.append(sum([cent[key] for key in keys if key in cent]))
        per = np.array(per)
        per = per / per.sum()

        for i in range(n):
            M[i] = A[i] / A[i].sum()
        M = M.T
        d = 0.85 # 1-선호도
        R = np.ones(n) / n
        # P = np.ones(n) / n
        P = per
        e = 1
        while e > 1e-7:
            R_ = d * M @ R + (1 - d) * P
            e = np.linalg.norm(R_ - R)
            R = R_

        index = np.argsort(R)[::-1][:3]

        for i in index:
            result.append(sentences[i])

    return result

########################################################################################################################
