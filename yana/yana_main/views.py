from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest 
from django.template import loader
from . import tasks
import threading
import logging
logger = logging.getLogger(__name__)
# Create your views here.


def getHome(requst:HttpRequest):
    toret =HttpResponse("Currently implementing, come back soon !")
    toret.status_code=200
    return toret