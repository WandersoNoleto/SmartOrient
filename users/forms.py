from django import forms

from users.models import Advisor, Coordination, Student


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["full_name", "course", "institution", "email", "phone_number", "enrollment", "password"]

class AdvisorRegisterForm(forms.ModelForm):
    class Meta:
        model = Advisor
        fields = ["full_name", "email", "phone_number", "institution", "enrollment", "password"]

class CoordinationRegisterForm(forms.ModelForm):
    class Meta:
        model = Coordination
        fields = ["course", "institution", "campus","code","email", "password"]



