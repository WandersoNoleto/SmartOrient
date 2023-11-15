from django.shortcuts import redirect, render

from guidances.models import Guidance
from users.models import Advisor, Coordination, Student


def guidance_register_save(request):
    if request.method == "POST":
        project_title       = request.POST.get("project_title")
        student_name       = request.POST.get("student")
        advisor_name       = request.POST.get("advisor")
        coordination_code  = request.POST.get("coordination")

        student      = Student.objects.filter(full_name=student_name).first()
        advisor      = Advisor.objects.filter(full_name=advisor_name).first()
        coordination = Coordination.objects.filter(code=coordination_code).first()

        guidance = Guidance(
            project_title = project_title,
            student      = student,
            advisor      = advisor,
            coordination = coordination,
            status       = "Em andamento"
        )

        guidance.set_start_date()
        guidance.generate_guidance_code()
        guidance.save()

    return redirect("Home")
