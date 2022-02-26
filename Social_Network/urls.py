"""Social_Network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Social_Network.views import home, sign_up,sign_in, sign_out, comparacion
from Social_Network.scraping import amazon, ebay
from bs4 import BeautifulSoup
import requests
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from django.conf.urls import url

#from Social_Network.scripting import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('signup', sign_up),
    path('signin/', sign_in),
    path('signout/', sign_out),
    path('try/', comparacion),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),

]