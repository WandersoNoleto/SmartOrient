from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.forms import (AdvisorRegisterForm, CoordinationRegisterForm,
                         StudentRegisterForm)
from users.models import Advisor, Coordination, Student


def login_student(request):
    if request.method == "POST":
        email    = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("Home")
        else:
            return render(request, 'login/login-student.html', {'error_message': 'Credenciais incorretas'})

    return render(request, 'login/login-student.html')



def register_student_page(request):
    formStudent = StudentRegisterForm

    context = {'formStudent': formStudent}

    return render(request, 'register/register-student.html', context)



def register_student_save(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        course    = request.POST.get("course")
        institution  = request.POST.get("institution")
        phone_number = request.POST.get("phone_number")
        enrollment   = request.POST.get("enrollment")
        password     = request.POST.get("password")
        email        = request.POST.get("email")

        student = Student.objects.create_user(
            full_name       = full_name, 
            course          = course,
            institution     = institution,
            phone_number    = phone_number,
            enrollment      = enrollment,
            password        = password, 
            email           = email
        )

        student.save()

    return redirect("login_student")



def login_advisor(request):
    if request.method == "POST":
        email     = request.POST.get("email")
        password  = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Orientador logado com sucesso") 
        else:
            return render(request, 'login/login-advisor.html', {'error_message': 'Credenciais incorretas'})

    return render(request, 'login/login-advisor.html')



def register_advisor_page(request):
    formAdvisor = AdvisorRegisterForm

    context = {'formAdvisor': formAdvisor}

    return render(request, 'register/register-advisor.html', context)



def register_advisor_save(request):
    if request.method == "POST":
        full_name    = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        enrollment   = request.POST.get("enrollment")
        institution  = request.POST.get("institution")
        password     = request.POST.get("password")
        email        = request.POST.get("email")

        advisor = Advisor.objects.create_user(
            full_name       = full_name, 
            phone_number    = phone_number,
            enrollment      = enrollment,
            institution     = institution,
            password        = password, 
            email           = email
        )

        advisor.save()

    return redirect("login_advisor")



def login_coordination(request):
    if request.method == "POST":
        email    = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Coordenação logado com sucesso") 
        else:
            return render(request, 'login/login-coordination.html', {'error_message': 'Credenciais incorretas'})

    return render(request, 'login/login-coordination.html')



def register_coordination_page(request):
    formCoordination = CoordinationRegisterForm

    context = {'formCoordination': formCoordination}

    return render(request, 'register/register-coordination.html', context)



def register_coordination_save(request):
    if request.method == "POST":
        institution   = request.POST.get("institution")
        campus       = request.POST.get("campus")
        code         = request.POST.get("code")
        password     = request.POST.get("password")
        email        = request.POST.get("email")

        coordination = Coordination.objects.create_user(
            institution = institution, 
            campus     = campus,
            code       = code,
            password   = password, 
            email      = email
        )

        coordination.save()

    return redirect("login_coordination")

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("Home")