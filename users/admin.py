from django.contrib import admin

from users.models import Advisor, Coordination, Student

admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(Coordination)
