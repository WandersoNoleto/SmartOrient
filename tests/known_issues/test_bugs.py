"""Functional bugs found in the 2023 code. Each test states the expected behavior and fails today (strict xfail).

Model-level bugs live next to the model tests (tests/*/test_models.py) with the same marker.
When a fix makes one of them pass, remove its xfail marker and move it next to the app's tests.
"""

import pytest
from django.contrib.auth.models import AnonymousUser, Group
from django.urls import reverse

from guidances.models import Guidance
from library.models import GuidanceArticle
from tests.factories import (
    PASSWORD,
    AdvisorFactory,
    CoordinationFactory,
    GuidanceFactory,
    StudentFactory,
)
from users.context_processors import logged_user
from users.models import Coordination, Student

pytestmark = [pytest.mark.django_db, pytest.mark.xfail(reason="known bug")]

PENDING, IN_PROGRESS = "Pendente", "Em andamento"

STUDENT_DATA = {
    "full_name": "Maria Lima",
    "course": "ECOMP",
    "institution": "IFPI",
    "phone_number": "1",
    "enrollment": "1",
    "password": "uma-senha-bem-forte-123",
    "email": "maria@example.com",
}


class TestRegistration:
    def test_role_groups_are_created_by_the_migrations(self):
        assert Group.objects.filter(name__in=["Students", "Advisors", "Coordinations"]).count() == 3

    def test_a_duplicated_email_shows_a_form_error(self, client, role_groups):
        StudentFactory(email=STUDENT_DATA["email"])

        response = client.post(reverse("register_student_save"), STUDENT_DATA)

        assert response.status_code == 200
        assert Student.objects.count() == 1

    def test_a_missing_field_shows_a_form_error(self, client, role_groups):
        response = client.post(reverse("register_student_save"), {"email": "x@example.com", "password": PASSWORD})

        assert response.status_code == 200
        assert not Student.objects.exists()

    def test_coordination_registration_keeps_the_course(self, client, role_groups):
        client.post(
            reverse("register_coordination_save"),
            {
                "course": "ECOMP",
                "institution": "IFPI",
                "campus": "THE",
                "code": "IFPI.THE-ECOMP",
                "password": "uma-senha-bem-forte-123",
                "email": "coord@example.com",
            },
        )

        assert Coordination.objects.get().course == "ECOMP"


class TestLogin:
    def test_login_honors_the_next_parameter(self, client):
        student = StudentFactory()
        target = reverse("register_guidance_page")

        response = client.post(
            f"{reverse('login_student')}?next={target}", {"email": student.email, "password": PASSWORD}
        )

        assert response.url == target


class TestGuidanceRequest:
    def test_an_unknown_advisor_shows_a_form_error(self, student_client):
        response = student_client.post(reverse("register_guidance_save"), {"project_title": "x", "advisor": "Ninguém"})

        assert response.status_code == 200
        assert not Guidance.objects.exists()

    def test_the_advisor_is_picked_by_id_not_by_name(self, student_client):
        AdvisorFactory(full_name="João Silva")
        chosen = AdvisorFactory(full_name="João Silva")

        student_client.post(
            reverse("register_guidance_save"),
            {"project_title": "x", "advisor": chosen.pk, "coordination": CoordinationFactory().pk},
        )

        assert Guidance.objects.get().advisor == chosen

    def test_the_student_sees_their_pending_requests(self, student_client, student):
        pending = GuidanceFactory(student=student)

        assert pending.guidance_code in student_client.get(reverse("Home")).content.decode()

    def test_refusing_a_request_does_not_reuse_the_delete_action(self, advisor_client, advisor):
        guidance = GuidanceFactory(advisor=advisor)

        content = advisor_client.get(reverse("guidances_pending_page")).content.decode()

        assert reverse("delete_guidance", args=[guidance.id]) not in content


class TestGuidancePage:
    def test_a_guidance_without_documents_opens(self, student_client, student):
        guidance = GuidanceFactory(student=student, status=IN_PROGRESS)

        assert student_client.get(reverse("open_guidance", args=[guidance.id])).status_code == 200

    def test_deleting_an_unknown_guidance_returns_404(self, advisor_client):
        assert advisor_client.post(reverse("delete_guidance", args=[999])).status_code == 404

    def test_uploaded_document_titles_drop_the_extension(self, student_client, student):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from tests.factories import MINIMAL_PDF

        guidance = GuidanceFactory(student=student, status=IN_PROGRESS)

        student_client.post(
            reverse("save_guidance_article", args=[guidance.id]),
            {"title": "Capitulo1.pdf", "file": SimpleUploadedFile("Capitulo1.pdf", MINIMAL_PDF)},
        )

        assert GuidanceArticle.objects.get().title == "Capitulo1"


class TestDashboards:
    def test_coordination_home_does_not_print_debug_output(self, coordination_client, capsys):
        coordination_client.get(reverse("home_coordination"))

        assert capsys.readouterr().out == ""


class TestPerformance:
    def test_the_logged_user_context_needs_at_most_one_query(self, rf, django_assert_max_num_queries):
        request = rf.get("/")
        request.user = CoordinationFactory()

        with django_assert_max_num_queries(1):
            logged_user(request)

    def test_anonymous_requests_do_not_query_the_logged_user(self, rf, django_assert_num_queries):
        request = rf.get("/")
        request.user = AnonymousUser()

        with django_assert_num_queries(0):
            logged_user(request)
