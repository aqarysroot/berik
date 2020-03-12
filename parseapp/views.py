from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ContentSerializer
# Create your views here.
from rest_framework.response import Response

import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

class MyClass(object):
    def __init__(self, text):
        self.text = text

my_objects = []

def scape():
    session = requests.Session()
    session.header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15"}
    url = 'http://bcomshop.kz/aksessuari-dlja-pk/adaptery'
    content = session.get(url, verify= False).content
    soup = BeautifulSoup(content, 'html.parser')
    # print(soup.find_all('div', {'class':'product-list'}))

    for item in soup.find_all('div', {'class':'product-list'}):
        for item2 in item.find_all('div', {'class': 'thumb_rating'}):
            my_objects.append(MyClass(item2.text.strip()))
    
    return my_objects

 
class ContentViewSet(viewsets.ViewSet):
    serializer_class = ContentSerializer
    def list(self, request):
        serializer = ContentSerializer(
            instance=scape(), many=True)
        return Response(serializer.data)
