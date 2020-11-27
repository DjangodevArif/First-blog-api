from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, Post, Coment, Co_coment

# Login page style.
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form','placeholder':'Password'}))

#

class Userregister(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form','placeholder':'Email'}))
    first_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form','placeholder':'Firstname'}))
    last_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form','placeholder':'Lastname'}))
    
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','first_name','last_name',
        'password1','password2',]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email

from django.contrib.auth.forms import PasswordResetForm
class PasswordReset(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'','placeholder': 'Email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)
        if not test:
            raise forms.ValidationError('Your email is not Registerd')
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'Email'}))
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
     
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name',]


        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','country']


class NewPostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['post_img','post_title','post_detail']

class ComentForm(forms.ModelForm):
    coment_detail = forms.CharField(widget=forms.Textarea(attrs={'rows':1}))
    class Meta:
        model = Coment
        fields = ['coment_detail',]


class Co_comentForm(forms.ModelForm):
    coment_detail = forms.CharField(widget=forms.Textarea(attrs={'rows':2,}))
    class Meta:
        model = Co_coment
        fields = ['coment_detail']

class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_img','post_title','post_detail']