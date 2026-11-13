import datetime

import pytest
from django.db import IntegrityError
from django.urls import NoReverseMatch, reverse

from guidances.models import Guidance
from tests.factories import (
    AdvisorFactory,
    CoordinationFactory,
    GuidanceArticleFactory,
    GuidanceFactory,
)

pytestmark = pytest.mark.django_db

PENDING, IN_PROGRESS = "Pendente", "Em andamento"


class TestRegisterGuidancePage:
    def test_lists_every_advisor_and_coordination_to_pick_from(self, student_client):
        advisors = AdvisorFactory.create_batch(2)
        coordinations = CoordinationFactory.create_batch(2)

        content = student_client.get(reverse("register_guidance_page")).content.decode()

        for advisor in advisors:
            assert advisor.full_name in content
        for coordination in coordinations:
            assert coordination.code in content

    def test_is_restricted_to_students(self, advisor_client, client):
        assert advisor_client.get(reverse("register_guidance_page")).status_code == 403
        client.logout()
        assert client.get(reverse("register_guidance_page")).url.startswith("/auth/login/")


class TestRegisterGuidanceSave:
    def post(self, client, **data):
        return client.post(reverse("register_guidance_save"), data)

    def test_creates_a_pending_guidance_for_the_logged_student(self, student_client, student):
        advisor = AdvisorFactory(full_name="Carlos Henrique Mendes")
        coordination = CoordinationFactory(code="IFPI.THE-ECOMP")

        response = self.post(
            student_client, project_title="Meu TCC", advisor="Carlos Henrique Mendes", coordination="IFPI.THE-ECOMP"
        )

        assert response.url == reverse("Home")
        guidance = Guidance.objects.get()
        assert (guidance.student, guidance.advisor, guidance.coordination) == (student, advisor, coordination)
        assert (guidance.project_title, guidance.status) == ("Meu TCC", PENDING)
        assert guidance.start_date == datetime.date.today()
        assert len(guidance.guidance_code) == 6

    def test_coordination_is_optional(self, student_client):
        advisor = AdvisorFactory()

        self.post(student_client, project_title="Meu TCC", advisor=advisor.full_name, coordination="")

        assert Guidance.objects.get().coordination is None

    def test_picks_the_first_advisor_when_names_collide(self, student_client):
        first = AdvisorFactory(full_name="João Silva")
        AdvisorFactory(full_name="João Silva")

        self.post(student_client, project_title="Meu TCC", advisor="João Silva")

        assert Guidance.objects.get().advisor == first

    def test_crashes_for_an_unknown_advisor(self, student_client):
        with pytest.raises(IntegrityError):
            self.post(student_client, project_title="Meu TCC", advisor="Ninguém")

    def test_anonymous_post_is_not_redirected_to_login_and_crashes(self, client):
        advisor = AdvisorFactory()

        with pytest.raises(IntegrityError):
            self.post(client, project_title="Meu TCC", advisor=advisor.full_name)

    def test_any_role_can_post(self, advisor_client):
        other_advisor = AdvisorFactory()

        with pytest.raises(IntegrityError):  # the advisor is not a student, so student is None
            self.post(advisor_client, project_title="Meu TCC", advisor=other_advisor.full_name)

    def test_get_only_redirects(self, student_client):
        assert student_client.get(reverse("register_guidance_save")).url == reverse("Home")
        assert not Guidance.objects.exists()


class TestPendingGuidancesPage:
    def test_lists_the_advisors_pending_requests(self, advisor_client, advisor):
        mine = GuidanceFactory(advisor=advisor)
        GuidanceFactory(advisor=advisor, status=IN_PROGRESS)
        GuidanceFactory()

        response = advisor_client.get(reverse("guidances_pending_page"))

        assert list(response.context["pending_guidances"]) == [mine]
        content = response.content.decode()
        assert mine.student.full_name in content
        assert reverse("pending_guidance_accept", args=[mine.id]) in content
        assert reverse("delete_guidance", args=[mine.id]) in content

    def test_anonymous_users_get_403_instead_of_a_login_redirect(self, client):
        assert client.get(reverse("guidances_pending_page")).status_code == 403

    def test_other_roles_are_forbidden(self, student_client):
        assert student_client.get(reverse("guidances_pending_page")).status_code == 403


class TestAcceptGuidance:
    def test_moves_a_pending_guidance_to_in_progress(self, advisor_client, advisor):
        guidance = GuidanceFactory(advisor=advisor)

        response = advisor_client.get(reverse("pending_guidance_accept", args=[guidance.id]))

        assert response.url == reverse("home_advisor")
        guidance.refresh_from_db()
        assert guidance.status == IN_PROGRESS

    def test_leaves_other_statuses_untouched(self, advisor_client, advisor):
        guidance = GuidanceFactory(advisor=advisor, status="Concluída")

        advisor_client.get(reverse("pending_guidance_accept", args=[guidance.id]))

        guidance.refresh_from_db()
        assert guidance.status == "Concluída"

    def test_returns_404_for_an_unknown_guidance(self, advisor_client):
        assert advisor_client.get(reverse("pending_guidance_accept", args=[999])).status_code == 404

    @pytest.mark.parametrize("who", ["anonymous", "student", "other_advisor"])
    def test_anyone_can_accept_any_guidance(self, client, who):
        guidance = GuidanceFactory()
        if who == "student":
            client.force_login(guidance.student)
        elif who == "other_advisor":
            client.force_login(AdvisorFactory())

        client.get(reverse("pending_guidance_accept", args=[guidance.id]))

        guidance.refresh_from_db()
        assert guidance.status == IN_PROGRESS


class TestDeleteGuidance:
    def test_deletes_the_guidance_and_its_articles(self, advisor_client, advisor):
        article = GuidanceArticleFactory(guidance__advisor=advisor)

        response = advisor_client.get(reverse("delete_guidance", args=[article.guidance.id]))

        assert response.url == reverse("home_advisor")
        assert not Guidance.objects.exists()

    def test_unknown_ids_just_redirect(self, advisor_client):
        assert advisor_client.get(reverse("delete_guidance", args=[999])).status_code == 302

    def test_anonymous_users_can_delete_any_guidance_with_a_get(self, client):
        guidance = GuidanceFactory(status=IN_PROGRESS)

        client.get(reverse("delete_guidance", args=[guidance.id]))

        assert not Guidance.objects.exists()


class TestOpenGuidance:
    def test_shows_the_guidance_details_and_the_latest_article(self, student_client, student):
        guidance = GuidanceFactory(student=student, status=IN_PROGRESS)
        GuidanceArticleFactory(guidance=guidance, title="Capitulo1.pdf")
        latest = GuidanceArticleFactory(guidance=guidance, title="Capitulo2.pdf")

        response = student_client.get(reverse("open_guidance", args=[guidance.id]))

        content = response.content.decode()
        for text in (guidance.guidance_code, guidance.project_title, guidance.advisor.full_name, "Capitulo1.pdf"):
            assert text in content
        assert response.context["articles"].last() == latest
        assert reverse("view_pdf", args=[latest.id]) in content
        assert reverse("save_guidance_article", args=[guidance.id]) in content

    def test_crashes_when_the_guidance_has_no_articles(self, student_client, student):
        guidance = GuidanceFactory(student=student, status=IN_PROGRESS)

        with pytest.raises(NoReverseMatch):
            student_client.get(reverse("open_guidance", args=[guidance.id]))

    def test_returns_404_for_an_unknown_guidance(self, student_client):
        assert student_client.get(reverse("open_guidance", args=[999])).status_code == 404

    def test_anyone_can_open_any_guidance(self, client):
        article = GuidanceArticleFactory()

        response = client.get(reverse("open_guidance", args=[article.guidance.id]))

        assert response.status_code == 200
        assert article.guidance.project_title in response.content.decode()
