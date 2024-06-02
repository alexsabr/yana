from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader
from . import tasks
import threading
import logging
logger = logging.getLogger(__name__)
# Create your views here.


def scrap(requst:HttpRequest):
    logger.critical("before starting scraping")
    threading.Thread(target=tasks.start_scraping).start()
    logger.critical("After starting scraping")
    toret =HttpResponse("OK")
    toret.status_code=200
    return toret