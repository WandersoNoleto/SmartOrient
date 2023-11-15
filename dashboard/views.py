from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from guidances.models import Guidance
from users.models import Student


@login_required(login_url= '/auth/login/')
def home(request):
    guidances      = Guidance.objects.all()
    logged_user_id = request.user.id
    logged_user    = Student.objects.filter(genericuser_ptr_id=logged_user_id).first()

    context = {
        'guidances': guidances,
        'logged_user': logged_user
        }

    return render(request, 'base.html', context)
