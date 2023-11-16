from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from guidances.models import Guidance
from users.models import Advisor, Coordination, Student


@login_required(login_url= '/auth/login/')
def register_guidance_page(request):
    advisors = Advisor.objects.all()
    coordinations = Coordination.objects.all()

    context = {
        'advisors': advisors,
        'coordinations': coordinations
    }


    return render(request, 'registerGuidance.html', context)


def register_guidance_save(request):
    if request.method == "POST":
        project_title      = request.POST.get("project_title")
        logged_user_id     = request.user.id
        advisor_name       = request.POST.get("advisor")
        coordination_code  = request.POST.get("coordination")

        student      = Student.objects.filter(genericuser_ptr_id=logged_user_id).first()
        advisor      = Advisor.objects.filter(full_name=advisor_name).first()
        coordination = Coordination.objects.filter(code=coordination_code).first()

        guidance = Guidance(
            project_title = project_title,
            student       = student,
            advisor       = advisor,
            coordination  = coordination,
        )

        guidance.set_start_date()
        guidance.generate_guidance_code()
        guidance.save()

    return redirect("Home")
