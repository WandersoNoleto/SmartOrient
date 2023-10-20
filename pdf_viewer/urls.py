from django.contrib import admin
from django.urls import path

from pdf_viewer import views

urlpatterns = [
    path('pdf-viewer/', views.home, name="Home"),
    path('save-pdf/', views.save_pdf, name="save-pdf")
]