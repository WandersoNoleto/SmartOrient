from .models import Advisor, Coordination, Student


def logged_user(request):
    logged_user_id = request.user.id
    student = Student.objects.filter(genericuser_ptr_id=logged_user_id).first()
    advisor = Advisor.objects.filter(genericuser_ptr_id=logged_user_id).first()
    coordination = Coordination.objects.filter(genericuser_ptr_id=logged_user_id).first()

    if student:
        user = student
        identifier_field = user.abbreviate_name if user else ''
    elif advisor:
        user = advisor
        identifier_field = user.abbreviate_name if user else ''
    elif coordination:
        user = coordination
        identifier_field = user.code_format if user else ''


    return {'logged_user': user, 'user_identifier_field': identifier_field}
