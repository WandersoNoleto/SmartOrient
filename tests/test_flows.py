"""End-to-end journey through the real endpoints, as the three roles use the app today."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import NoReverseMatch, reverse

from guidances.models import Guidance
from library.models import GuidanceArticle
from tests.factories import MINIMAL_PDF, PASSWORD

pytestmark = pytest.mark.django_db


def register_and_login(save_url, login_url, data):
    client = Client()
    client.post(reverse(save_url), data | {"password": PASSWORD})
    response = client.post(reverse(login_url), {"email": data["email"], "password": PASSWORD})
    assert response.status_code == 302, f"{data['email']} could not log in"
    return client


def test_guidance_journey_from_request_to_deletion(role_groups):
    student = register_and_login(
        "register_student_save",
        "login_student",
        {
            "full_name": "Maria Eduarda Souza Lima",
            "course": "ECOMP",
            "institution": "IFPI",
            "phone_number": "1",
            "enrollment": "2023001",
            "email": "maria@example.com",
        },
    )
    advisor = register_and_login(
        "register_advisor_save",
        "login_advisor",
        {
            "full_name": "Carlos Henrique Mendes",
            "phone_number": "1",
            "enrollment": "P1",
            "institution": "IFPI",
            "email": "carlos@example.com",
        },
    )
    coordination = register_and_login(
        "register_coordination_save",
        "login_coordination",
        {
            "course": "ECOMP",
            "institution": "IFPI",
            "campus": "THE",
            "code": "IFPI.THE-ECOMP",
            "email": "coord@example.com",
        },
    )

    # Student requests the guidance: it stays hidden from their home while pending
    student.post(
        reverse("register_guidance_save"),
        {
            "project_title": "Gamificação no ensino de lógica",
            "advisor": "Carlos Henrique Mendes",
            "coordination": "IFPI.THE-ECOMP",
        },
    )
    guidance = Guidance.objects.get()
    assert guidance.guidance_code not in student.get(reverse("Home")).content.decode()

    # Advisor sees the request and accepts it
    assert "Maria Eduarda Souza Lima" in advisor.get(reverse("guidances_pending_page")).content.decode()
    advisor.get(reverse("pending_guidance_accept", args=[guidance.id]))
    assert guidance.guidance_code in student.get(reverse("Home")).content.decode()
    assert guidance.guidance_code in advisor.get(reverse("home_advisor")).content.decode()
    assert "Gamificação no ensino de lógica" in coordination.get(reverse("home_coordination")).content.decode()

    # The guidance page crashes until it has a document, so the first upload cannot come from the UI
    with pytest.raises(NoReverseMatch):
        student.get(reverse("open_guidance", args=[guidance.id]))
    student.post(
        reverse("save_guidance_article", args=[guidance.id]),
        {"title": "Capitulo1.pdf", "file": SimpleUploadedFile("Capitulo1.pdf", MINIMAL_PDF)},
    )
    article = GuidanceArticle.objects.get()
    assert "Capitulo1.pdf" in student.get(reverse("open_guidance", args=[guidance.id])).content.decode()
    assert advisor.get(reverse("view_pdf", args=[article.id])).status_code == 200

    # Advisor removes the guidance, everything goes with it; student logs out
    advisor.get(reverse("delete_guidance", args=[guidance.id]))
    assert not Guidance.objects.exists()
    assert not GuidanceArticle.objects.exists()
    student.get(reverse("custom_logout"))
    assert student.get(reverse("Home")).status_code == 302
