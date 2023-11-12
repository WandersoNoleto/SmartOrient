from hashlib import sha256

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from users.models import Advisor, Coordination, Student


def login_student(request):
    if request.method == "POST":
        email  = request.POST.get("email")
        password    = request.POST.get("password")

        student = authenticate(request, email=email, password=password)
        if student is not None:
            login(request, student)
            return redirect("Home")  
        else:
            return render(request, 'login/login-student.html', {'error_message': 'Credenciais incorretas'})

    return render(request, 'login/login-student.html')

def register_student_page(request):
    return render(request, 'register/register-student.html')

def register_student_save(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        course    = request.POST.get("course")
        phone_number = request.POST.get("phone_number")
        enrollment   = request.POST.get("enrollment")
        password     = request.POST.get("password")
        email        = request.POST.get("email")

        student = Student.objects.create_user(
            full_name       = full_name, 
            course          = course, 
            phone_number    = phone_number,
            enrollment      = enrollment,
            password        = password, 
            email           = email
        )

        student.save()


    return redirect("login_student")
