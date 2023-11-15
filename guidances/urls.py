from django.urls import path

from guidances import views

urlpatterns = [
    path('guidance-register-save/', views.guidance_register_save, name="guidance_register_save")

]