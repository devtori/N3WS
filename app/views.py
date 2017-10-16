from django.shortcuts import render
import csv
from django.http import HttpResponse
from app.models import *
from . import zmycode
from . import zsoncode
from collections import Counter


def index(request):
    return render(request, 'app/index.html', {})

def result(request, value):
    result = []
    url_list = []
    zsoncode.search_cache_db(value)
    caches = Cache.objects.filter(word = value).values('url', 'sentence1', 'sentence2', 'sentence3','num')
    variables = {'value': value, 'result':result, 'url_list':url_list, 'caches': caches}
    return render(request, 'app/news_list.html', variables)


def cloud(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']='attachment; filename="words.csv"'
    keywords = []
    newses = News.objects.all().values('keyword1', 'keyword2', 'keyword3').order_by('-id')[:1000]
    for news in newses:
        for i in range(1, 4):
            keyword = news['keyword{}'.format(i)]
            if keyword:
                keywords.append(keyword)
    count = Counter(keywords)
    data = count.most_common(50)
    mm = max([d[1] for d in data])
    data = [(word, freq / mm) for word, freq in data]
    writer = csv.writer(response)
    writer.writerow(['word', 'freq'])
    writer.writerows(data)
    return response
