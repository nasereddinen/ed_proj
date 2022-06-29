from dataclasses import field
from pyexpat import model
from socket import fromshare
from unicodedata import category
from django.forms import ModelForm, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.forms.formsets import formset_factory

class Studentloginform(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
                "placeholder": "Addresse e-mail..",
                "class": "form-control",
            }
        ),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                "placeholder": "Mot De Pass...",
                "class": "form-control",
            }
        ),)

class TeacherLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
                "placeholder": "Addresse e-mail...",
                "class": "form-control",
            }
        ),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                "placeholder": "Mot De Pass...",
                "class": "form-control",}
        ),)

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
                "placeholder": "ecrire votre Nom..",
                "class": "form-control",
            }
        ),)
    email = forms.CharField(widget=forms.TextInput(attrs={
                "placeholder": "Ecrire votre email..",
                "class": "form-control",
            }
        ),)
   
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
                "placeholder": "saisie votre mot de pass...",
                "class": "form-control",
            }
        ),)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                "placeholder": "veuillez ecrire votre mot de pass...",
                "class": "form-control",
            }
        ),)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

class resumeForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        field = '__all__'
        exclude = ['user','follows']

           
class Annonce_Form(forms.ModelForm):
    class Meta:
        model = annonce
        field = '__all__'
        exclude = ['author']
class Cours_Form(forms.ModelForm):
  
    class Meta:
        model = cours
        field = '__all__'
        exclude =['teacher','like','likes','date']

class video_Form(ModelForm):
    class Meta:
        model = VideoCours
        field = '__all__'
        exclude =['cour']
        

Formset_vid = formset_factory(video_Form,extra=1)
#question form
class question_Form(ModelForm):
    class Meta:
        model=question
        field = '__all__'
        exclude=['author']
class Blog_Form(ModelForm):
    class Meta:
        model=blog
        fields = ('title','category','desc')
        labels={
            'title': ('titre'),
        }
class Subject_form(ModelForm):
    class Meta:
        model=Sujet
        fileds=( 'title','images')
        exclude=['author']
class Note_Form(ModelForm):
    class Meta:
        model=notes
        exclude = ['chapitre','student']
        labels={
            'text_note': (''),
        }
        