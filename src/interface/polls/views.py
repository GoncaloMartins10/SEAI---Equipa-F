from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    latest_question_list = ["Hello", "World", "Vicente" ]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)