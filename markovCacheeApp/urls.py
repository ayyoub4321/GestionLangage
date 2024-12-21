from .views import *
from django.urls import path

urlpatterns = [
    path("", index , name="index"),
    path('genre',genre,name="genre1"),
]
