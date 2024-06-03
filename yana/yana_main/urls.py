from django.urls import path
from . import views
urlpatterns = [
    path("",views.getHome, name="home"), # hook to launch scrapping, vowed to disappear.
    
]