from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.db import models


class GenericUserManager(UserManager):
    def create_user(self, **extra_fields):
        return self._create_user(**extra_fields)

class GenericUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = GenericUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email 

class Student(GenericUser):
    full_name    = models.CharField(max_length=50, verbose_name="Nome Completo")
    course       = models.CharField(max_length=50, verbose_name="Curso")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula")
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")

    def __str__(self):
        return self.full_name
    
class Advisor(GenericUser):
    full_name    = models.CharField(max_length=50, verbose_name="Nome Completo")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula") 
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")

    def __str__(self):
        return self.full_name
    

class Coordination(GenericUser):
    course      = models.CharField(max_length=50, verbose_name="Curso")
    institution = models.CharField(max_length=50, verbose_name="Instituição")
    campus      = models.CharField(max_length=50, verbose_name="Campus")
    code        = models.CharField(unique=True, help_text="Unique per coordination: institution.campus-course", max_length=50, verbose_name="Código")

    def __str__(self):
        return self.code

