from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout

from django.contrib import messages
from .models import *
from study_portal_app.forms import *

from youtubesearchpython import VideosSearch

import requests

import json
# Create your views here.

def signup(request):
    if request.method=="POST":
        form = Signup(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successfully!')
            return HttpResponseRedirect(reverse('study_portal_app:login'))
    else:
        form = Signup()
    context={
        'form': form,
    }
    return render(request, 'signup.html', context)

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return HttpResponseRedirect(reverse('study_portal_app:index'))
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request,"login.html", context={"form":form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('study_portal_app:login'))


def profile(request):
    hw=HomeWork.objects.filter(user=request.user, status=False)
    if len(hw)==0:
        hw_c=True
    else:
        hw_c=False
    context={
        'hw': hw,
        'hw_c': hw_c,
    }
    return render(request, 'profile.html', context)

def index(request):
    note_obj = Note.objects.filter(user=request.user)
    if request.method=="POST":
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note_form.save(commit=False)
            note_form = request.user
            note_form.save()
            messages.success(request, 'Your data has been submited! ')
            return HttpResponseRedirect(reverse('study_portal_app:index'))
    else:
        note_form = NoteForm()
    context = {
        'note_obj': note_obj,
        'note_form': note_form,
    }
    return render(request, 'index.html', context)

def delete_note(request, pk):
    delte_obj=Note.objects.get(id=pk).delete()
    messages.warning(request, 'Your NOTE has been deleted Successfully!')
    return HttpResponseRedirect(reverse('study_portal_app:index'))

def homework(request):
    hw_obj = HomeWork.objects.filter(user=request.user)
    if request.method=="POST":
        form = form = HomeWorkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['status']
                if finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            homeworks = HomeWorkForm(
                user =request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                status = finished
            )
            homeworks.save()
            messages.success(request, 'Your HomeWork Added Successfully!!')
            return HttpResponseRedirect(reverse('study_portal_app:index'))
    else:
        form = HomeWorkForm()

    if len(hw_obj)== 0:
        hw_finished=True
    else:
        hw_finished=False
    context = {
        'hw_obj': hw_obj,
        'hw_finished': hw_finished,
        'form': form,
    }
    return render(request, 'homework.html', context)


def homework_update(request, pk):
    hw_update = HomeWork.objects.get(id=pk)
    if hw_update.status==True:
        hw_update.status=False
    else:
        hw_update.status = True
    hw_update.save()
    return HttpResponseRedirect(reverse('study_portal_app:homework'))


def youtube(request):
    if request.method=="POST":
        form = Youtube(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'publish': i['publishedTime'],
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context={
                'form': form,
                'result_list': result_list,
            }
        return render(request, 'youtube.html', context)
    else:
        form = Youtube
    context={
        'form': form,
    }
    return render(request, 'youtube.html', context)

def todo(request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form = request.user
            form.save()
            return HttpResponse('done')
    else:
        form = TodoForm()

    todo_obj=Todo.objects.filter(user=request.user)
    context={
        'todo_obj': todo_obj,
        'form': form,
    }
    return render(request, 'todo.html', context)

def todo_update(request, pk):
    todo_update = Todo.objects.get(id=pk)
    if todo_update.status == True:
        todo_update.status=False
    else:
        todo_update.status = True
    todo_update.save()
    return HttpResponseRedirect(reverse('study_portal_app:todo'))


def book(request):
    form = Book()
    if request.method=="POST":
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        ans=r.json()
        result_list=[]
        for i in range(10):
            resutl_dic={
                'title':ans['items'][i]['volumeInfo']['title'],
                'subtitle':ans['items'][i]['volumeInfo'].get('subtitle'),
                'description':ans['items'][i]['volumeInfo'].get('description'),
                'count':ans['items'][i]['volumeInfo'].get('pageCount'),
                'rating':ans['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':ans['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':ans['items'][i]['volumeInfo'].get('previewLink'),
        }
            result_list.append(resutl_dic)
            context={
                'form': form,
                'result_list': result_list
            }
        return render(request, 'book.html', context)

    context= {
        'form': form,
    }
    return render(request, 'book.html', context)
