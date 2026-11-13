import pytest
from django.urls import reverse

from tests.factories import AdvisorFactory, CoordinationFactory, GuidanceFactory, StudentFactory

pytestmark = pytest.mark.django_db

IN_PROGRESS = "Em andamento"

# (url name, factory of the role allowed in)
DASHBOARDS = [
    ("Home", StudentFactory),
    ("home_advisor", AdvisorFactory),
    ("home_coordination", CoordinationFactory),
]


@pytest.mark.parametrize(("url_name", "factory_class"), DASHBOARDS)
def test_anonymous_users_are_sent_to_the_student_login(client, url_name, factory_class):
    response = client.get(reverse(url_name))

    assert response.url == f"/auth/login/?next={reverse(url_name)}"


@pytest.mark.parametrize(
    ("url_name", "other_factory"),
    [(url_name, other) for url_name, owner in DASHBOARDS for _, other in DASHBOARDS if other is not owner],
)
def test_other_roles_are_forbidden(client, url_name, other_factory):
    client.force_login(other_factory())

    assert client.get(reverse(url_name)).status_code == 403


def test_home_is_served_at_the_root_and_under_dashboard(student_client):
    assert reverse("Home") == "/dashboard/"
    assert student_client.get("/").status_code == 200


class TestStudentHome:
    def test_lists_only_the_students_guidances_in_progress(self, student_client, student):
        mine = GuidanceFactory(student=student, status=IN_PROGRESS)
        pending = GuidanceFactory(student=student)
        others = GuidanceFactory(status=IN_PROGRESS)

        response = student_client.get(reverse("Home"))

        assert list(response.context["guidances"]) == [mine]
        content = response.content.decode()
        assert mine.guidance_code in content
        assert pending.guidance_code not in content
        assert others.guidance_code not in content

    def test_shows_the_advisor_and_links_to_the_guidance(self, student_client, student):
        guidance = GuidanceFactory(student=student, status=IN_PROGRESS)

        content = student_client.get(reverse("Home")).content.decode()

        assert guidance.advisor.full_name in content
        assert reverse("open_guidance", args=[guidance.id]) in content

    def test_header_shows_the_abbreviated_name(self, client):
        client.force_login(StudentFactory(full_name="Maria Eduarda Souza Lima"))

        assert "Maria E. S. Lima" in client.get(reverse("Home")).content.decode()


class TestAdvisorHome:
    def test_lists_in_progress_guidances_and_counts_pending_ones(self, advisor_client, advisor):
        in_progress = GuidanceFactory(advisor=advisor, status=IN_PROGRESS)
        GuidanceFactory.create_batch(2, advisor=advisor)
        GuidanceFactory(status=IN_PROGRESS)

        response = advisor_client.get(reverse("home_advisor"))

        assert list(response.context["guidances"]) == [in_progress]
        assert response.context["pending_guidances"].count() == 2
        content = response.content.decode()
        assert in_progress.guidance_code in content
        assert in_progress.student.full_name in content


class TestCoordinationHome:
    def test_lists_the_coordinations_guidances_in_progress(self, coordination_client, coordination):
        mine = GuidanceFactory(coordination=coordination, status=IN_PROGRESS)
        GuidanceFactory(coordination=coordination)
        GuidanceFactory(status=IN_PROGRESS)

        response = coordination_client.get(reverse("home_coordination"))

        assert list(response.context["guidances"]) == [mine]
        assert mine.project_title_format() in response.content.decode()

    def test_header_shows_the_course_and_institution(self, coordination_client, coordination):
        content = coordination_client.get(reverse("home_coordination")).content.decode()

        assert coordination.course in content
        assert coordination.institution in content
