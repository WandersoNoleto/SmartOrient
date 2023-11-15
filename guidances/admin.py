from django.contrib import admin

from guidances.models import Guidance


class GuidanceAdmin(admin.ModelAdmin):
    list_display = ('project_type', 'project_title', 'student', 'advisor', 'coordination', 'guidance_code')

    def save_model(self, request, obj, form, change):
        if not obj.guidance_code:
            obj.guidance_code = obj.generate_guidance_code()

        super().save_model(request, obj, form, change)

admin.site.register(Guidance, GuidanceAdmin)