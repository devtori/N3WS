from konlpy.tag import Twitter
from collections import Counter
import crawling

crawling.main()

t = Twitter()
import csv
import codecs

#text = codecs.open('new.txt','r','utf-8')
#text = open('new.txt')
#doc_ko = text.read()
doc_ko = open('new.txt').read() #'codecs를 사용해서 읽어오려니까 오류도 많이 생기고 text에서 doc_ko로 넘어가는 과정이 한번 더 생겨서 하나로 줄임

# 단어 대체하기
replace_dic = {'추천':'','베스트':'','기사':'','칼럼':'','동아':'','직후':'','올해':'','때문':'','관련':'','대한':'','따위':'','따름':'','나위':'','대로':''
               ,'만큼':'','마리':'','가마':'','묶음':'','바리':'','오늘':'','내일':'','듯이':'','종류':'','테야':'','사람':'','그릇':'','덩어리':'','발자국':''
               ,'군데':'','채로':'','이것':'','저것':'','그루':'','무엇':'','우리':'','누구':'','너희':'','어디':'','언제':'','통해':'','이하':'','이상':''
               ,'위한':'','일부':'','해당':'','다음':'','이전':'','경우':'','최후':'','기자':'','등등':'','켤레':'','자루':'','미터':'','마일':''
               ,'센치':'','센티':'','킬로미터':'','등지':'','내지':'','위해':'','위하여':'','대해':'','에서':'','가장':'','최근':'','라며':'','정도':''
               ,'다른':'','같은':'','지금':'','현재':'','당시':'','동안':'','다시':'','처음':'','단지':'','크게':'','작게':'','가운데':'','보기':'','모든':''
               ,'물론':'','실제':'','주요':'','대부분':'','비롯':'','비록':'','여기':'','저기':'','한편':'','그동안':'','지난':'','특별':'','아직':'','바로':''
               ,'또한':'','중이':'','중인':'','다만':'','본격':'','적극':'','까지':'','더욱':'','얘기':'','로부터':'','주변':'','년대':'','내부':'','인근':''
               ,'향후':'','먼저':'','해도':'','그대로':'','별로':'','이제':'','여부':'','매우':'','아주':'','모두':'','넉달':''}

def swap(document, dic):
    for Xword in document:
        if len(Xword)==1: #단어의 길이가 1일 경우
            index = document.index(Xword)
            document[index] = document[index].replace(Xword,'') #단어삭제
        elif Xword in dic: #그외의 경우
            index = document.index(Xword)
            document[index] = document[index].replace(Xword, dic[Xword]) #대체가능한 단어 적어놓은 것 중에서 실행
    return document

#token

def text2pos(silsigan):
    contentPos = []
    word_tag_pairs = t.pos(silsigan, norm=True, stem=True)
    keywords = [word for word, tag in word_tag_pairs if tag == 'Noun']
    contentPos.extend(keywords)
    return swap(contentPos, replace_dic)

token = text2pos(doc_ko)

FreqDict = Counter(token)
#print('Counter : ', FreqDict.most_common(100))
FreqDict[''] = 0 #FreqDict 안에 ''의 빈도수값을 0으로 바꿔버림
data = FreqDict.most_common(50)  #token 빈도값을 기준으로 내림차순으로 정리 ( most_common(n)을 하게 되면, 상위 n개의 빈도값과 token만을 의미 )
#data = data[1:51] #상위 2번째 부터 51번째까지만 들어갈 수 있도록 설정(필요없는 단어를 ''로 바꿀때, ''값이 너무 커져서 워드클라우드 생성 안되므로)

with codecs.open('words.csv', 'w', encoding='utf-8') as f:
    f.write('word,freq\n')
    writer = csv.writer(f)
    writer.writerows(data)
