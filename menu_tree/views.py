from django.shortcuts import render

# Create your views here.

def main_page(request, path=None):
    return render(request, 'main_page.html')
