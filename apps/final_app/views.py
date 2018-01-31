from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages

def index(request):
    return render(request, 'final_app/index.html')

def add(request):
    result = User.objects.registration_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
            return redirect('/')
    else:
        request.session['user_id'] = result.id
        request.session['name'] = result.name
        request.session['alias'] = result.alias
    return redirect('/homepage')

def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        request.session['name'] = result.name
        request.session['alias'] = result.alias
    return redirect('/homepage')

def homepage(request):
    if not 'user_id' in request.session:
        return redirect('/main')
    user = User.objects.get(id = request.session["user_id"])
    context = {
        'users': User.objects.all(),
        'count': Poke.objects.count()
    }
    return render(request, 'final_app/homepage.html', context)

def poke(request, id):
    user = User.objects.get(id = id)
    count = Poke.objects.get(id = id)
    count.users.add(user)
    newPoke = Poke.objects.create()
    return redirect('/homepage')


def logout(request):
    del request.session
    return redirect('/')

