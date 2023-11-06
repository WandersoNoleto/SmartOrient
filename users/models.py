from django.db import models


class Student(models.Model):
    full_name    = models.CharField(max_length=50, verbose_name="Nome Completo")
    course       = models.CharField(max_length=50, verbose_name="Curso")
    email        = models.EmailField(max_length=50, verbose_name="Email")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula") 
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")

    def __str__(self):
        return self.full_name
    
class Advisor(models.Model):
    full_name    = models.models.CharField(max_length=50, verbose_name="Nome Completo")
    email        = models.EmailField(max_length=50, verbose_name="Email")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula") 
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")

    def __str__(self):
        return self.full_name
