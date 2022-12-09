from django.forms import ModelForm
from .models import Listing
from django.contrib.auth.models import User
from django import forms
from taggit.forms import TagField, TagWidget


class ListingForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "text",
        "placeholder": "Example: Senior Laravel Developer",
    }), label="")

    tags = TagField(widget=TagWidget(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "text",
        "placeholder": "Example: Laravel, Backend, Postgres, etc",
    }), label="")

    company = forms.CharField(widget=forms.TextInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "text",
        "placeholder": "",
    }), label="")

    location = forms.CharField(widget=forms.TextInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "text",
        "placeholder": "Example: Remote, Boston MA, etc",
    }), label="")

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "text",
        "placeholder": "",
    }), label="")

    website = forms.CharField(widget=forms.TextInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "text",
        "placeholder": "eg. abc.net",
    }), label="")

    logo = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "file",
        "placeholder": "",
    }), label="")

    description = forms.CharField(widget=forms.TextInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "textarea",
        "placeholder": "Include tasks, requirements, salary, etc",
    }), label="")


    class Meta:
        model = Listing
        fields = '__all__'


        widgets = {
            'tags': TagWidget()
        }


class RegisterForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "text",
        "placeholder": "",
    }), label="")


    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "email",
        "placeholder": "",
    }), label="")

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "border border-gray-200 rounded p-2 w-full",
        "type": "password",
        "placeholder": "",
    }), label="")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']