from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse


def test_page(request):
    return HttpResponse('<h1>That\'s great!</h1>')
