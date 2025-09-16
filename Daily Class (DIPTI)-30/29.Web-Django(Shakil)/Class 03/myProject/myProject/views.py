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
    return render(request, 'home.html',tableDict)

def about(request):
    tableDict = {
        'cmpName': 'Google',
        'cmpContact': '012342',
        'country': 'USA',
        
        'cmpName1': 'Microsoft',
        'cmpContact1': '1211',
        'country1': 'Bangladesh',
    }
    return render(request, 'about.html',tableDict)

