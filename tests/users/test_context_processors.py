import pytest
from django.contrib.auth.models import AnonymousUser

from tests.factories import AdvisorFactory, CoordinationFactory, StudentFactory
from users.context_processors import logged_user
from users.models import GenericUser

pytestmark = pytest.mark.django_db


def context_for(rf, user):
    request = rf.get("/")
    request.user = user
    return logged_user(request)


@pytest.mark.parametrize("factory_class", [StudentFactory, AdvisorFactory])
def test_students_and_advisors_are_identified_by_their_abbreviated_name(rf, factory_class):
    user = factory_class(full_name="Maria Eduarda Souza Lima")

    context = context_for(rf, user)

    assert context["logged_user"] == user
    assert isinstance(context["logged_user"], factory_class._meta.model)
    # The bound method is passed (not its result); the template engine calls it when rendering
    assert context["user_identifier_field"]() == "Maria E. S. Lima"


def test_coordinations_are_identified_by_their_code(rf):
    coordination = CoordinationFactory(code="IFPI.THE-ECOMP")

    assert context_for(rf, coordination) == {"logged_user": coordination, "user_identifier_field": "IFPI.THE-ECOMP"}


def test_users_without_a_role_profile_get_an_empty_context(rf):
    admin = GenericUser.objects.create_superuser("admin@example.com", "s3nha-forte")

    assert context_for(rf, admin) == {"logged_user": None, "user_identifier_field": ""}


def test_anonymous_users_get_an_empty_context(rf):
    assert context_for(rf, AnonymousUser()) == {"logged_user": None, "user_identifier_field": ""}


def test_runs_three_queries_on_every_request(rf, django_assert_num_queries):
    user = CoordinationFactory()

    with django_assert_num_queries(3):
        context_for(rf, user)
