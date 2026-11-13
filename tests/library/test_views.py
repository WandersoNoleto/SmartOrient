import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from library.models import GuidanceArticle
from tests.factories import MINIMAL_PDF, GuidanceFactory

pytestmark = pytest.mark.django_db


def upload(client, guidance_id, name="Capitulo1.pdf", content=MINIMAL_PDF, title=None):
    return client.post(
        reverse("save_guidance_article", args=[guidance_id]),
        {"title": name if title is None else title, "file": SimpleUploadedFile(name, content)},
    )


def test_saves_the_file_and_redirects_back_to_the_guidance(student_client, student):
    guidance = GuidanceFactory(student=student, status="Em andamento")

    response = upload(student_client, guidance.id)

    assert response.url == reverse("open_guidance", kwargs={"id": guidance.id})
    article = GuidanceArticle.objects.get()
    assert article.guidance == guidance
    assert article.file.name.startswith("guidance_articles/Capitulo1")
    with article.file.open("rb") as stored:
        assert stored.read() == MINIMAL_PDF


def test_keeps_the_extension_in_the_title(student_client, student):
    guidance = GuidanceFactory(student=student)

    upload(student_client, guidance.id)

    assert GuidanceArticle.objects.get().title == "Capitulo1.pdf"


def test_accepts_any_file_type(student_client, student):
    guidance = GuidanceFactory(student=student)

    upload(student_client, guidance.id, name="virus.exe", content=b"MZ")

    assert GuidanceArticle.objects.get().file.name.endswith(".exe")


def test_anonymous_users_can_upload_to_any_guidance(client):
    upload(client, GuidanceFactory().id)

    assert GuidanceArticle.objects.count() == 1


def test_returns_404_for_an_unknown_guidance(student_client):
    assert upload(student_client, 999).status_code == 404


def test_get_only_redirects(student_client, student):
    guidance = GuidanceFactory(student=student)

    response = student_client.get(reverse("save_guidance_article", args=[guidance.id]))

    assert response.url == reverse("open_guidance", kwargs={"id": guidance.id})
    assert not GuidanceArticle.objects.exists()
