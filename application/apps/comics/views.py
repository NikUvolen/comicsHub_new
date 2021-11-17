from django.shortcuts import render
from django.http import HttpResponse


def test_page(request):
    return HttpResponse('<h1>Comics is active</h1>')
