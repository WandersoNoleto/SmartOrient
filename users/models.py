from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import GenericUserManager


class GenericUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    
    objects = GenericUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    def abbreviate_name(self):
        parts = self.full_name.split()

        if len(parts) < 3:
            return self.full_name

        abbreviated = [parts[0]] + [f"{name[0]}." if name.lower() not in {"e", "de"} else name for name in parts[1:-1]] + [parts[-1]]
        abbreviated_name = ' '.join(abbreviated)

        return abbreviated_name

    def __str__(self):
        return self.email 

class Student(GenericUser):
    full_name    = models.CharField(max_length=50, verbose_name="Nome Completo")
    course       = models.CharField(max_length=50, verbose_name="Curso")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula")
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")
    institution  = models.CharField(max_length=50, verbose_name="Instituição")

    def __str__(self):
        return self.full_name
    
class Advisor(GenericUser):
    full_name    = models.CharField(max_length=50, verbose_name="Nome Completo")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula") 
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")
    institution = models.CharField(max_length=50, verbose_name="Instituição")

    def __str__(self):
        return self.full_name
    

class Coordination(GenericUser):
    course      = models.CharField(max_length=50, verbose_name="Curso")
    institution = models.CharField(max_length=50, verbose_name="Instituição")
    campus      = models.CharField(max_length=50, verbose_name="Campus")
    code        = models.CharField(unique=True, help_text="Unique per coordination: institution.campus-course", max_length=50, verbose_name="Código: institution.campus-course")

    def __str__(self):
        return self.code

