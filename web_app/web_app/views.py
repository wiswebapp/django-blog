import re
#I Have Created This File - Webster
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # return HttpResponse("<h1>Hello From Webster !</h1>")
    return render(request, 'index2.html')

def makeupper(request):
    textString = request.POST.get('analyzeText', 'default')
    ignoreSpecialCase = request.POST.get('ignoreSpecialCase', 'off')
    actualText = textString

    if ignoreSpecialCase == "on":
        textString = re.sub(r'[^\w\s]', '', textString)

    analyzeText = textString.upper()

    params = {
        'actualText': actualText,
        'analyzeText': analyzeText,
    }
    return render(request, 'make_upper.html', params)
