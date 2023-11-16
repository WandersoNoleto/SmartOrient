from django.urls import path

from guidances import views

urlpatterns = [
    path('register-guidance-page/student', views.register_guidance_page, name="register_guidance_page"),
    path('register-guidance-save/', views.register_guidance_save, name="register_guidance_save"),
]