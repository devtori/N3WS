from django.shortcuts import render

def index(request):
    return render(request, 'app/index.html', {})

def test(request, value):
    return render(request, 'app/test.html', {})
