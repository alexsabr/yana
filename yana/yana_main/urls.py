from django.urls import path
from . import views
urlpatterns = [
    path("article",views.getHome, name="home"), 
    path("number",views.number_articles_available, name="article_number"), 
    path("",views.number_articles_available)
]