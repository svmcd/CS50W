from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")


def samed(request):
    return HttpResponse("Hallo Samed!")

def polat(request):
    return HttpResponse("Hallo Polat!")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize
    })


