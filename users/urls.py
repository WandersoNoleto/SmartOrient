from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.login_student, name="login_student"),
    path('register/student/', views.register_student_page, name="register_student_page"),
    path('register/student/save/', views.register_student_save, name="register_student_save"),

    path('login/advisor/', views.login_advisor, name="login_advisor"),
    path('register/advisor/', views.register_advisor_page, name="register_advisor_page"),
    path('register/advisor/save/', views.register_advisor_save, name="register_advisor_save"),

    path('login/coordination/', views.login_coordination, name="login_coordination"),
    path('register/coordination/', views.register_coordination_page, name="register_coordination_page"),
    path('register/coordination/save/', views.register_coordination_save, name="register_coordination_save"),

    path('logout/', views.custom_logout, name="custom_logout")
]