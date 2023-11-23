from django.urls import path

from pdf_viewer import views

urlpatterns = [
    path("pdfViewer/<int:id>/", views.view_pdf, name="view_pdf"),
]