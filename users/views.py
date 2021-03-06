from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView 
from django.contrib.auth.models import User
from django.http import HttpResponse 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from users.forms import LoginForm, SignupForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUp(View):
    
    def get(self, request):
        form=SignupForm()
        return render(request,'users/signup.html',{'form':form})
    def post(self,request):
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect('users:login')
        else:
            return render(request,'users/signup.html',{'form':form})
    

class Login(View):

    def get(self,request):
        form=LoginForm()
        return render(request,'users/login.html',{'form':form})
    def post(self,request):
        redirect_url=request.GET.get('next')
        form=LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect('/')

            else:
                return HttpResponse('brak uzytkownika')
        return HttpResponse('cos poszlo nie tak')


class Logout(View):
    def get(selq,request):
        logout(request)
        return redirect('users:login')


