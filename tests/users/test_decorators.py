import pytest
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse

from tests.factories import AdvisorFactory, StudentFactory
from users.decorators import user_has_permission

pytestmark = pytest.mark.django_db


@user_has_permission(allowed_roles=["Students", "Coordinations"])
def protected_view(request):
    return HttpResponse("ok")


def request_for(rf, user):
    request = rf.get("/")
    request.user = user
    return request


def test_lets_an_allowed_role_through(rf):
    response = protected_view(request_for(rf, StudentFactory()))

    assert (response.status_code, response.content) == (200, b"ok")


def test_forbids_a_role_that_is_not_allowed(rf):
    response = protected_view(request_for(rf, AdvisorFactory()))

    assert response.status_code == 403
    assert "Você não tem permissão" in response.content.decode()


def test_forbids_a_user_without_any_group(rf):
    assert protected_view(request_for(rf, StudentFactory(in_role_group=False))).status_code == 403


def test_forbids_anonymous_users_instead_of_redirecting_to_login(rf):
    assert protected_view(request_for(rf, AnonymousUser())).status_code == 403


def test_keeps_the_view_metadata():
    assert protected_view.__name__ == "protected_view"
