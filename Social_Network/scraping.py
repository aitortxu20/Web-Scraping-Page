from bs4 import BeautifulSoup
import requests
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.contrib import messages
import os

#HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

def amazon(request,element):

    global html_codes
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36' } #We use headers to see that the request for Amazon has been made by an human.
    amazon_content = {}
    ebay_content = {}
    ebay_content2 = {}

    #First, we scrap in Amazon.
    url = 'https://www.amazon.es/s?k='+element+'&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2Z6LJDRVYPCRN&sprefix='+element+'%2Caps%2C116&ref=nb_sb_noss_1'
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content,'lxml')
    amazon_prices = []
    amazon_titles = []
    dict_amazon = []
    contador_amazon = 0
    url_list = []
    tags = []
    buttons = []
    count_image = 0
    count_button = 0
    html_codes = [] #This is for the background image in /try/  path

    #We scrap the title from Amazon.
    try:
        #First we get the title of the element.
        title = soup.find_all('span',
                            attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})
        #Then we get the price.
        price = soup.find_all('span',
                          attrs={'class': 'a-price-whole'})
        #Finally we get the image
        image = soup.find_all('img',
                              attrs={'class':'s-image'})

        for image_tag in image:
            count_image += 1
            if count_image < 4:
                tags.append(image_tag['src'])

        for titles in title:
            contador_amazon += 1
            if contador_amazon < 4:
                amazon_titles.append(titles.text)


            else:
                contador_amazon = 0
                break
        for prices in price:
            contador_amazon += 1
            if contador_amazon < 4:
                amazon_prices.append(prices.text + '$')


        for elemento in range(len(amazon_titles)):
            url = url + amazon_titles[elemento]
            url = url.replace(' ','')
            #We create an html code for each Amazon Search of the element.
            doc = """ <html>
            <body>
                <h2> AMAZON: </h2>
                <div class="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20" data-asin="B07TTJR48G" data-index="1" data-uuid="ad272963-2afb-4a53-bdd9-d4ebb0b33d9e" data-height="100px">
    
                <span class="a-size-base-plus a-color-base a-text-normal">
                    {}: <h2>Precio: {}</h2>
                    <img src={} width="150px" >
                  
                </span>  
                <form action={}>
                    <button type="submit">🔗</button>
                </form> 
            </body>
            </html>
                                        
            """.format(amazon_titles[elemento],amazon_prices[elemento],tags[elemento],url)
            html_codes.append(doc)
            html_codes.append('\n')

        #We make a dictionary where the key is the title and the value is the price.
        dict_amazon = dict(zip(amazon_titles,amazon_prices))


    except AttributeError:
        title_string = 'NA'
        print('product Title = ', title_string)
        return render(request,
                      '/app/Social_Network/Autentication/home.html')

    return dict_amazon,url,tags,html_codes,render(request, '/app/Social_Network/Autentication/home.html')
    #return t.render(ctx)


def ebay(request,element):

    #This function is the same we do for amazon but now for ebay.
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    url = 'https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw='+element+'&_sacat=0'
    webpage2 = requests.get(url, headers=HEADERS)
    soup2 = BeautifulSoup(webpage2.content, 'lxml')
    ebay_prices = []
    ebay_titles = []
    dict_ebay = []
    tags = []
    buttons = []
    contador_ebay = 0
    count_image = 0
    count_button = 0

    try:
        title_ebay = soup2.find_all('h3',
                               attrs={'class': 's-item__title'})


        prices_ebay = soup2.find_all('span',
                                attrs={'class': 's-item__price'})

        image = soup2.find_all('img',
                              attrs={'class': 's-item__image-img'})

        url_button = soup2.find_all('a',
                              attrs={'class': 's-item__link'})

        for url_buttons in url_button:
            count_button += 1
            if count_button < 4:
                buttons.append(url_buttons['href'])

        for image_tag in image:
            count_image += 1
            if count_image < 4:
                tags.append(image_tag['src'])
        for titles_ebay in title_ebay:
            contador_ebay += 1
            if titles_ebay.text != '':
                if contador_ebay < 4:
                    ebay_titles.append(titles_ebay.text)
                else:
                    contador_ebay = 0
                    break
        for price_in_ebay in prices_ebay:
            contador_ebay += 1
            if contador_ebay < 6:
                ebay_prices.append(price_in_ebay.text)


        for elemento in range(len(ebay_titles)):
            url = url + ebay_titles[elemento]
            url = url.replace(' ', '')
            doc = """ <html>
            <body>
            <div style="text-align:left">
                <font size=6 color="red">EBAY:</font>
                <div class="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20" data-asin="B07TTJR48G" data-index="1" data-uuid="ad272963-2afb-4a53-bdd9-d4ebb0b33d9e" data-height="100px">

                <span class="a-size-base-plus a-color-base a-text-normal">
                    {}: <h2>Precio: {}</h2>
                    <img src={} width="150px" >

                </span>  
                <form action={}>
                    <button type="submit">🔗</button>
                </form> 
            </div>    
            </body>
            </html>

            """.format(ebay_titles[elemento], ebay_prices[elemento], tags[elemento], buttons[elemento])
            html_codes.append(doc)
            html_codes.append('\n')

        dict_ebay = dict(zip(ebay_titles,ebay_prices))

    except AttributeError:
        title_string = 'NA'
        print('product Title = ', title_string)
        return render(request,
                      '/app/Social_Network/Autentication/scraper.html')
    return dict_ebay,render(request,
              '/app/Social_Network/Autentication/scraper.html')



