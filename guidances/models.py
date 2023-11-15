import random
from datetime import datetime
from string import ascii_uppercase, digits

from django.db import models

from users.models import Advisor, Coordination, Student


class Guidance(models.Model):

    project_title = models.CharField(max_length=100, verbose_name="Título do projeto")
    student       = models.ForeignKey(Student, on_delete=models.CASCADE, max_length=100, blank=False, null=False, verbose_name="Estudante")
    advisor       = models.ForeignKey(Advisor, on_delete=models.CASCADE, max_length=100, blank=False, null=False, verbose_name="Orientador")
    coordination  = models.ForeignKey(Coordination, on_delete=models.SET_NULL, max_length=100, blank=True, null=True, verbose_name="Coordenação")
    status        = models.CharField(max_length=50, default="Em andamento", verbose_name="Status")
    start_date    = models.DateField(verbose_name="Data de início")
    guidance_code = models.CharField(max_length=6, unique=True, verbose_name="Código Da Orientação")


    def generate_guidance_code(self):
        generated_code =  ''.join(random.choice(ascii_uppercase + digits) for _ in range(6))
        self.guidance_code = generated_code
    
    def set_start_date(self):
        date = datetime.now().strftime("%Y-%m-%d")
        self.start_date = date


    def save(self, *args, **kwargs):
        if not self.guidance_code:
            self.guidance_code = self.generate_guidance_code()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.guidance_code
    
