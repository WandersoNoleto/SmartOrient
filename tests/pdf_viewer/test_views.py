import pytest
from django.urls import reverse

from tests.factories import GuidanceArticleFactory

pytestmark = pytest.mark.django_db


def test_renders_the_viewer_pointing_to_the_media_url(student_client):
    article = GuidanceArticleFactory(title="Capitulo1.pdf")

    content = student_client.get(reverse("view_pdf", args=[article.id])).content.decode()

    assert "Capitulo1.pdf" in content
    assert f'id="pdfUrl" value="{article.file.url}"' in content
    assert "/media/pdf.js/build/pdf.js" in content


def test_returns_404_for_an_unknown_article(student_client):
    assert student_client.get(reverse("view_pdf", args=[999])).status_code == 404


def test_anyone_can_view_any_article(client):
    article = GuidanceArticleFactory()

    assert client.get(reverse("view_pdf", args=[article.id])).status_code == 200
