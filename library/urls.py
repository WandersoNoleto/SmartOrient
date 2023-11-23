from django.urls import path

from library import views

urlpatterns = [
    path("save-guidance-article/<int:guidance_id>/", views.save_guidance_article, name="save_guidance_article")   
]