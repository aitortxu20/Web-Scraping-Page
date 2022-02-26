from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from Social_Network.scraping import amazon , ebay
import os

def home(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template = open(os.path.join(BASE_DIR, 'Autentication/home.html'))
    return render(request, template)

def get_element(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        element = request.POST['element']
    return element
    return render(request, os.path.join(BASE_DIR, 'Autentication/home.html'))

def sign_up(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    return render(request, os.path.join(BASE_DIR, 'Autentication/sign_up.html'))


def sign_in(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, os.path.join(BASE_DIR, 'Autentication/home.html'), {'fname':fname})

        else:
            messages.error(request, 'Bad Credentials')
            return redirect('/home/')

    return render(request, os.path.join(BASE_DIR, 'Autentication/sign_in.html'))


def sign_out(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logout(request)
    messages.success(request, 'Logged Out Succesfully!')
    return redirect('/home/')
    return render(request, os.path.join(BASE_DIR, 'Autentication/sign_out.html'))

def comparacion(request):
    messages.success(request,request.method)
    if request.method == 'POST':
        element = request.POST['element']
        #Amazon
        amazon(request,element)
        url_list = []
        dic,url,image_tag,codes, rend = amazon(request,element)
        keys = []
        values = []
        for k,v in dic.items():
            keys.append(k)
            values.append(v)
        final_dict = dict(zip(keys,values))
        #Ebay
        ebay(request,element)
        dic_ebay, rende = ebay(request,element)
        ebay_keys = []
        ebay_values = []
        for k, v in dic_ebay.items():
            ebay_keys.append(k)
            ebay_values.append(v)

        ebay_final_dict = dict(zip(ebay_keys, ebay_values))

    return HttpResponse(codes)

   # return render(request, '/home/kali/Desktop/Scripts/Django/Social_Network/Social_Network/Autentication/home.html',context={'final_dict':final_dict, 'ebay_final_dict':ebay_final_dict, 'image_tag':image_tag, 'codes':codes})
