from django.urls import path
from . import views
urlpatterns = [
    path("",views.scrap, name="scrapit"), # hook to launch scrapping, vowed to disappear.
    
]