import pytest
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.urls import reverse

from tests.factories import PASSWORD, AdvisorFactory, CoordinationFactory, StudentFactory
from users.models import Advisor, Coordination, Student

pytestmark = pytest.mark.django_db

STUDENT_DATA = {
    "full_name": "Maria Eduarda Souza Lima",
    "course": "Engenharia de Computação",
    "institution": "IFPI",
    "phone_number": "86999990000",
    "enrollment": "2023001",
    "password": PASSWORD,
    "email": "maria@example.com",
}
ADVISOR_DATA = {
    "full_name": "Carlos Henrique Albuquerque Mendes",
    "phone_number": "86999990001",
    "enrollment": "P001",
    "institution": "IFPI",
    "password": PASSWORD,
    "email": "carlos@example.com",
}
COORDINATION_DATA = {
    "course": "Engenharia de Computação",
    "institution": "IFPI",
    "campus": "THE",
    "code": "IFPI.THE-ECOMP",
    "password": PASSWORD,
    "email": "coord@example.com",
}

# (save url, login url name, model, group, post data)
REGISTRATIONS = [
    ("register_student_save", "login_student", Student, "Students", STUDENT_DATA),
    ("register_advisor_save", "login_advisor", Advisor, "Advisors", ADVISOR_DATA),
    ("register_coordination_save", "login_coordination", Coordination, "Coordinations", COORDINATION_DATA),
]

# (login url name, factory, redirect url name)
LOGINS = [
    ("login_student", StudentFactory, "Home"),
    ("login_advisor", AdvisorFactory, "home_advisor"),
    ("login_coordination", CoordinationFactory, "home_coordination"),
]


class TestRegisterPages:
    @pytest.mark.parametrize(
        ("url_name", "fields"),
        [
            ("register_student_page", ["full_name", "course", "institution", "email", "phone_number", "enrollment"]),
            ("register_advisor_page", ["full_name", "email", "phone_number", "institution", "enrollment"]),
            ("register_coordination_page", ["course", "institution", "campus", "code", "email"]),
        ],
    )
    def test_render_one_input_per_form_field(self, client, url_name, fields):
        response = client.get(reverse(url_name))

        assert response.status_code == 200
        for field in [*fields, "password"]:
            assert f'name="{field}"' in response.content.decode()

    def test_render_the_password_as_a_plain_text_input(self, client):
        content = client.get(reverse("register_student_page")).content.decode()

        assert 'type="text" class="form-control" placeholder="Password" name="password"' in content


class TestRegisterSave:
    @pytest.mark.parametrize(("save_url", "login_url", "model", "group", "data"), REGISTRATIONS)
    def test_creates_the_user_in_its_role_group_and_redirects_to_its_login(
        self, client, role_groups, save_url, login_url, model, group, data
    ):
        response = client.post(reverse(save_url), data)

        assert response.status_code == 302
        assert response.url == reverse(login_url)
        user = model.objects.get(email=data["email"])
        assert user.check_password(PASSWORD)
        assert list(user.groups.values_list("name", flat=True)) == [group]

    def test_coordination_registration_drops_the_course(self, client, role_groups):
        client.post(reverse("register_coordination_save"), COORDINATION_DATA)

        assert Coordination.objects.get().course == ""

    @pytest.mark.parametrize(("save_url", "login_url", "model", "group", "data"), REGISTRATIONS)
    def test_get_only_redirects(self, client, save_url, login_url, model, group, data):
        response = client.get(reverse(save_url))

        assert response.url == reverse(login_url)
        assert not model.objects.exists()

    @pytest.mark.parametrize(("save_url", "login_url", "model", "group", "data"), REGISTRATIONS)
    def test_crashes_when_the_role_group_does_not_exist_leaving_a_user_without_group(
        self, client, save_url, login_url, model, group, data
    ):
        with pytest.raises(Group.DoesNotExist):
            client.post(reverse(save_url), data)

        assert not model.objects.get(email=data["email"]).groups.exists()

    def test_crashes_on_a_duplicated_email(self, client, role_groups):
        StudentFactory(email=STUDENT_DATA["email"])

        with pytest.raises(IntegrityError):
            client.post(reverse("register_student_save"), STUDENT_DATA)

    def test_accepts_any_password_and_blank_fields(self, client, role_groups):
        blank = dict.fromkeys(STUDENT_DATA, "") | {"email": "x@example.com", "password": "1"}

        client.post(reverse("register_student_save"), blank)

        student = Student.objects.get(email="x@example.com")
        assert student.check_password("1")
        assert student.full_name == ""

    def test_crashes_when_a_field_is_missing(self, client, role_groups):
        with pytest.raises(IntegrityError):
            client.post(reverse("register_student_save"), {"email": "x@example.com", "password": "1"})


class TestLogin:
    @pytest.mark.parametrize(("login_url", "factory_class", "home_url"), LOGINS)
    def test_get_renders_the_form(self, client, login_url, factory_class, home_url):
        response = client.get(reverse(login_url))

        assert response.status_code == 200
        assert 'name="email"' in response.content.decode()

    @pytest.mark.parametrize(("login_url", "factory_class", "home_url"), LOGINS)
    def test_logs_in_and_redirects_to_the_role_home(self, client, login_url, factory_class, home_url):
        user = factory_class()

        response = client.post(reverse(login_url), {"email": user.email, "password": PASSWORD})

        assert response.url == reverse(home_url)
        assert int(client.session["_auth_user_id"]) == user.pk

    @pytest.mark.parametrize(("login_url", "factory_class", "home_url"), LOGINS)
    def test_rejects_a_wrong_password(self, client, login_url, factory_class, home_url):
        user = factory_class()

        response = client.post(reverse(login_url), {"email": user.email, "password": "errada"})

        assert response.status_code == 200
        assert "Credenciais incorretas" in response.content.decode()
        assert "_auth_user_id" not in client.session

    def test_rejects_a_user_in_another_role_portal(self, client):
        advisor = AdvisorFactory()

        response = client.post(reverse("login_student"), {"email": advisor.email, "password": PASSWORD})

        assert "Credenciais incorretas" in response.content.decode()
        assert "_auth_user_id" not in client.session

    def test_ignores_the_next_parameter(self, client):
        student = StudentFactory()

        response = client.post(
            reverse("login_student") + "?next=/guidances/register-guidance-page/student",
            {"email": student.email, "password": PASSWORD},
        )

        assert response.url == reverse("Home")


class TestLogout:
    def test_logs_out_and_redirects_home(self, student_client):
        response = student_client.get(reverse("custom_logout"))

        assert response.url == reverse("Home")
        assert "_auth_user_id" not in student_client.session

    def test_anonymous_users_are_just_redirected(self, client):
        assert client.get(reverse("custom_logout")).url == reverse("Home")

    def test_works_with_get(self, student_client):
        assert student_client.get(reverse("custom_logout")).status_code == 302
