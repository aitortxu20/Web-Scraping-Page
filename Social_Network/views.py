from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from Social_Network.scraping import return_value, amazon
import os

def home(request):
    #It returns the main page (home.html)
    return render(request, '/app/Social_Network/Autentication/home.html')

def get_element(request):
    if request.method == 'POST':
        element = request.POST['element']
    return element
    return render(request, '/app/Social_Network/Autentication/home.html')

def sign_up(request):

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email= request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, 'Your account has been created {} !!! '.format(myuser.first_name))


        return redirect('signin/')

    return render(request, '/app/Social_Network/Autentication/sign_up.html')


def sign_in(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, '/app/Social_Network/Autentication/home.html', {'fname':fname})

        else:
            messages.error(request, 'Bad Credentials')
            return redirect('/home/')

    return render(request, '/app/Social_Network/Autentication/sign_in.html')


def sign_out(request):

    logout(request)
    messages.success(request, 'Logged Out Succesfully!')
    return redirect('/home/')
    return render(request, '/app/Social_Network/Autentication/sign_out.html')

def comparacion(request):

    messages.success(request,request.method)
    if request.method == 'POST':
        element = request.POST['element']
        amazon(element)
        #dict_amazon,buttons,tags = amazon(element)
        return HttpResponse(return_value)


    #return render(request, '/app/Social_Network/Autentication/home.html',context={'final_dict':dict_amazon,'image_tag':tags, 'button':buttons})
