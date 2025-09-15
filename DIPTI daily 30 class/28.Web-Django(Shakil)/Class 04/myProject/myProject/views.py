from django.shortcuts import render

def home(request):
    
    tableDict = {
        'cmpName': 'Google',
        'cmpContact': '012342',
        'country': 'USA',
        
        'cmpName1': 'Microsoft',
        'cmpContact1': '1211',
        'country1': 'Bangladesh',
    }
    return render(request, 'index.html',tableDict)

def about(request):
    return render(request, 'about.html')
def news(request):
    return render(request, 'news.html')

def contact(request):
    return render(request, 'contact.html')



