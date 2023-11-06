from django.urls import path

from users import views

urlpatterns = [
    path('', views.login_student, name="login_student"),
    path('register-student/', views.register_student_page, name="register_student_page"),
    path('register-student-save/', views.register_student_save, name="register_student_save")
]