from django import forms
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeWorkForm(forms.ModelForm):
    class Meta:
        model=HomeWork
        widgets= {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'status']

class Youtube(forms.Form):
    text = forms.CharField(max_length=100, label =' Enter your search')

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title', 'status']


class Book(forms.Form):
    text = forms.CharField(max_length=100, label =' Enter your Book')



class Signup(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
