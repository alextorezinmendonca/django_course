from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'recipes/home.html', context = {
                                                            'name': 'Alex',
                                                            
                                                            })


def contact(request):
    return render(request, 'delete_me/temp.html')


def about(request):
    return HttpResponse("about")    