from django.db import models


class Student(models.Model):
    full_name    = models.CharField(max_length=50, verbose_name="Nome Completo")
    course       = models.CharField(max_length=50, verbose_name="Curso")
    email        = models.EmailField(max_length=50, verbose_name="Email")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula")
    password     = models.CharField(max_length=50, default='',verbose_name="Senha") 
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")

    def __str__(self):
        return self.full_name
    
class Advisor(models.Model):
    full_name    = models.CharField(max_length=50, verbose_name="Nome Completo")
    email        = models.EmailField(max_length=50, verbose_name="Email")
    enrollment   = models.CharField(max_length=50, verbose_name="Matrícula") 
    password     = models.CharField(max_length=50, default='', verbose_name="Senha") 
    phone_number = models.CharField(max_length=50, verbose_name="Número de Telefone")

    def __str__(self):
        return self.full_name
    

class Coordination(models.Model):
    course      = models.CharField(max_length=50, verbose_name="Curso")
    institution = models.CharField(max_length=50, verbose_name="Instituição")
    campus      = models.CharField(max_length=50, verbose_name="Campus")
    code        = models.CharField(unique=True, help_text="Unique per coordination: institution.campus-course", max_length=50, verbose_name="Código")
    password    = models.CharField(max_length=50, default='', verbose_name="Senha") 

    def __str__(self):
        return self.code

