from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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

def guidances_pending_page(request):
    pending_guidances = Guidance.objects.filter(status="Pendente", advisor_id=request.user.id)

    context = {
        'pending_guidances': pending_guidances,
    }

    return render(request, 'acceptGuidance.html', context)

def pending_guidance_accept(request, id):
    guidance = get_object_or_404(Guidance, id=id)
    if guidance.status == "Pendente":
        guidance.status = "Em andamento"
        guidance.save()

    return redirect("home_advisor")

def delete_guidance(request, id):
    guidance = Guidance.objects.filter(id=id)
    guidance.delete()

    return redirect("home_advisor")