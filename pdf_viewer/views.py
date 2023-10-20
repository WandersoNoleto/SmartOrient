import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect, render


def home(request):
    pdf_file_name = "HIstoricoParcial.pdf"

    pdf_file_path = os.path.join(settings.MEDIA_ROOT, pdf_file_name)
    if os.path.exists(pdf_file_path):
        pdf_file_url = os.path.join(settings.MEDIA_URL, pdf_file_name)
        print(pdf_file_url)

        context = {
            'pdf_file_url': pdf_file_url
        }

    return render(request, 'test-pdf.html', context)

def save_pdf(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']

        file_name = default_storage.get_available_name(pdf_file.name)
        path = default_storage.save(file_name, ContentFile(pdf_file.read()))

    return redirect("Home")

