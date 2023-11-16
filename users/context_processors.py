from .models import Student


def logged_user(request):
    logged_user_id = request.user.id
    user = Student.objects.filter(genericuser_ptr_id=logged_user_id).first() if logged_user_id else None
    return {'logged_user': user, 'full_name': user.abbreviate_name if user else ''}
