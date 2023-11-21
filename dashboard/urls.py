
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('advisor/', views.home_advisor, name="home_advisor")
    
]

