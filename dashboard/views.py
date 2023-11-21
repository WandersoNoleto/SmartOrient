from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from guidances.forms import GuidanceRegisterForm
from guidances.models import Guidance
from users.models import Student


@login_required(login_url= '/auth/login/')
def home(request):
    guidances      = Guidance.objects.filter(status="Em andamento", student_id=request.user.id)
    logged_user_id = request.user.id
    logged_user    = Student.objects.filter(genericuser_ptr_id=logged_user_id).first()
    formGuidance   = GuidanceRegisterForm

    context = {
        'guidances': guidances,
        'logged_user': logged_user,
        'formGuidance': formGuidance
        }
    
    return render(request, 'studentHome.html', context)

@login_required(login_url= '/auth/login/')
def home_advisor(request):
    guidances        = Guidance.objects.filter(status="Em andamento", advisor_id=request.user.id)
    pending_guidances = Guidance.objects.filter(status="Pendente", advisor_id=request.user.id)
    logged_user_id = request.user.id
    logged_user    = Student.objects.filter(genericuser_ptr_id=logged_user_id).first()
    formGuidance   = GuidanceRegisterForm

    context = {
        'guidances': guidances,
        'logged_user': logged_user,
        'formGuidance': formGuidance,
        'pending_guidances': pending_guidances
        }
    
    return render(request, 'advisorHome.html', context)

