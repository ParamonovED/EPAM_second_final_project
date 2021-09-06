from django.urls import path
from . import views


app_name = "weather_check"
urlpatterns = [
    path('', views.main, name="main"),
    path('city', views.city, name="city"),
]
