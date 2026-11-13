"""Security issues found in the 2023 code. Each test states the expected behavior and fails today (strict xfail).

When a fix makes one of them pass, remove its xfail marker and move it next to the app's tests.
"""

import importlib

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from guidances.models import Guidance
from library.models import GuidanceArticle
from tests.factories import (
    MINIMAL_PDF,
    AdvisorFactory,
    GuidanceArticleFactory,
    GuidanceFactory,
    StudentFactory,
)
from users.models import Student

pytestmark = [pytest.mark.django_db, pytest.mark.xfail(reason="known security issue")]

PENDING, IN_PROGRESS = "Pendente", "Em andamento"


def assert_sent_to_login(response):
    assert response.status_code == 302
    assert response.url.startswith("/auth/login/")


class TestAuthenticationIsRequired:
    def test_accepting_a_guidance(self, client):
        guidance = GuidanceFactory()

        assert_sent_to_login(client.post(reverse("pending_guidance_accept", args=[guidance.id])))
        guidance.refresh_from_db()
        assert guidance.status == PENDING

    def test_deleting_a_guidance(self, client):
        guidance = GuidanceFactory()

        assert_sent_to_login(client.post(reverse("delete_guidance", args=[guidance.id])))
        assert Guidance.objects.filter(pk=guidance.pk).exists()

    def test_opening_a_guidance(self, client):
        article = GuidanceArticleFactory()

        assert_sent_to_login(client.get(reverse("open_guidance", args=[article.guidance.id])))

    def test_uploading_a_document(self, client):
        guidance = GuidanceFactory()

        client.post(
            reverse("save_guidance_article", args=[guidance.id]),
            {"title": "x.pdf", "file": SimpleUploadedFile("x.pdf", MINIMAL_PDF)},
        )

        assert not GuidanceArticle.objects.exists()

    def test_viewing_a_document(self, client):
        article = GuidanceArticleFactory()

        assert_sent_to_login(client.get(reverse("view_pdf", args=[article.id])))

    def test_requesting_a_guidance(self, client):
        advisor = AdvisorFactory()

        response = client.post(reverse("register_guidance_save"), {"project_title": "x", "advisor": advisor.full_name})

        assert_sent_to_login(response)

    def test_pending_page_redirects_anonymous_users_to_login(self, client):
        assert_sent_to_login(client.get(reverse("guidances_pending_page")))


class TestOnlyParticipantsHaveAccess:
    def test_only_the_guidance_advisor_can_accept_it(self, client):
        guidance = GuidanceFactory()
        client.force_login(AdvisorFactory())

        client.post(reverse("pending_guidance_accept", args=[guidance.id]))

        guidance.refresh_from_db()
        assert guidance.status == PENDING

    def test_students_cannot_accept_their_own_request(self, client):
        guidance = GuidanceFactory()
        client.force_login(guidance.student)

        client.post(reverse("pending_guidance_accept", args=[guidance.id]))

        guidance.refresh_from_db()
        assert guidance.status == PENDING

    def test_only_the_guidance_advisor_can_delete_it(self, client):
        guidance = GuidanceFactory()
        client.force_login(AdvisorFactory())

        client.post(reverse("delete_guidance", args=[guidance.id]))

        assert Guidance.objects.filter(pk=guidance.pk).exists()

    def test_other_students_cannot_open_a_guidance(self, client):
        article = GuidanceArticleFactory()
        client.force_login(StudentFactory())

        assert client.get(reverse("open_guidance", args=[article.guidance.id])).status_code in (403, 404)

    def test_other_students_cannot_view_its_documents(self, client):
        article = GuidanceArticleFactory()
        client.force_login(StudentFactory())

        assert client.get(reverse("view_pdf", args=[article.id])).status_code in (403, 404)

    def test_other_students_cannot_upload_to_it(self, client):
        guidance = GuidanceFactory(status=IN_PROGRESS)
        client.force_login(StudentFactory())

        client.post(
            reverse("save_guidance_article", args=[guidance.id]),
            {"title": "x.pdf", "file": SimpleUploadedFile("x.pdf", MINIMAL_PDF)},
        )

        assert not GuidanceArticle.objects.exists()

    def test_only_students_can_request_a_guidance(self, advisor_client):
        other_advisor = AdvisorFactory()

        response = advisor_client.post(
            reverse("register_guidance_save"), {"project_title": "x", "advisor": other_advisor.full_name}
        )

        assert response.status_code == 403


class TestStateChangesRequirePost:
    @pytest.mark.parametrize("url_name", ["pending_guidance_accept", "delete_guidance"])
    def test_guidance_actions_reject_get(self, advisor_client, advisor, url_name):
        guidance = GuidanceFactory(advisor=advisor)

        assert advisor_client.get(reverse(url_name, args=[guidance.id])).status_code == 405
        guidance.refresh_from_db()
        assert guidance.status == PENDING

    def test_logout_rejects_get(self, student_client):
        assert student_client.get(reverse("custom_logout")).status_code == 405


class TestUploads:
    def test_only_pdf_files_are_accepted(self, student_client, student):
        guidance = GuidanceFactory(student=student, status=IN_PROGRESS)

        student_client.post(
            reverse("save_guidance_article", args=[guidance.id]),
            {"title": "virus.exe", "file": SimpleUploadedFile("virus.exe", b"MZ")},
        )

        assert not GuidanceArticle.objects.exists()

    def test_a_renamed_file_is_not_taken_for_a_pdf(self, student_client, student):
        guidance = GuidanceFactory(student=student, status=IN_PROGRESS)

        student_client.post(
            reverse("save_guidance_article", args=[guidance.id]),
            {"title": "fake.pdf", "file": SimpleUploadedFile("fake.pdf", b"MZ not a pdf")},
        )

        assert not GuidanceArticle.objects.exists()


class TestAccounts:
    def test_register_form_hides_the_password(self, client):
        content = client.get(reverse("register_student_page")).content.decode()

        assert 'type="password"' in content

    def test_weak_passwords_are_rejected(self, client, role_groups):
        client.post(
            reverse("register_student_save"),
            {
                "full_name": "Maria Lima",
                "course": "x",
                "institution": "x",
                "phone_number": "1",
                "enrollment": "1",
                "password": "1",
                "email": "maria@example.com",
            },
        )

        assert not Student.objects.exists()


class TestSettings:
    def test_debug_false_in_the_environment_disables_debug(self, monkeypatch):
        import smartorient.settings as project_settings

        monkeypatch.setenv("DEBUG", "False")
        try:
            assert importlib.reload(project_settings).DEBUG is False
        finally:
            monkeypatch.undo()
            importlib.reload(project_settings)
