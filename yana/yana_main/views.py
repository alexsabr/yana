import random

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404,JsonResponse

from yana_scrap.models import article_db
from django.core import serializers
import logging
logger = logging.getLogger(__name__)
# Create your views here.





def getHome(request:HttpRequest):
    selected_article_pk=random.choice(article_db.objects.filter(linked_article__isnull=False).values_list("pk",flat=True))
    selected_article= {}
    try :
        selected_article=article_db.objects.get(pk=selected_article_pk)
    except article_db.DoesNotExist:
        raise Http404("Article not found ... Sorry!")

    toret =JsonResponse(selected_article.model_to_dict(recursive=True),safe=True)
    #toret.status_code=200
    return toret


def number_articles_available(request:HttpRequest):
    toret = {"number_article_available":article_db.objects.filter().count()}
    return JsonResponse(toret,safe=True)