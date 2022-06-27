from django.http import HttpResponse
from django.shortcuts import render

def HelloView(request):
    return HttpResponse("hi")