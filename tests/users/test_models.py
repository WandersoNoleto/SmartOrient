import pytest

from tests.factories import AdvisorFactory, CoordinationFactory, StudentFactory
from users.models import GenericUser

pytestmark = pytest.mark.django_db

NAMED_USER_FACTORIES = [StudentFactory, AdvisorFactory]


@pytest.mark.parametrize("factory_class", NAMED_USER_FACTORIES)
@pytest.mark.parametrize(
    ("full_name", "expected"),
    [
        ("Maria", "Maria"),
        ("Maria Lima", "Maria Lima"),
        ("Maria Eduarda Lima", "Maria E. Lima"),
        ("Maria Eduarda Souza Lima", "Maria E. S. Lima"),
        ("João Batista de Oliveira", "João B. de Oliveira"),
        ("Pedro e Paulo Santos", "Pedro e P. Santos"),
        ("Ana De Souza Costa", "Ana De S. Costa"),
    ],
)
def test_abbreviate_name_keeps_first_and_last_names_and_the_connectors_de_and_e(factory_class, full_name, expected):
    assert factory_class.build(full_name=full_name).abbreviate_name() == expected


@pytest.mark.parametrize("factory_class", NAMED_USER_FACTORIES)
def test_abbreviate_name_abbreviates_other_connectors(factory_class):
    assert factory_class.build(full_name="Ana da Silva Costa").abbreviate_name() == "Ana d. S. Costa"


@pytest.mark.xfail(reason="known bug: only 'de' and 'e' are kept, 'da', 'do', 'dos' and 'das' get abbreviated")
@pytest.mark.parametrize("factory_class", NAMED_USER_FACTORIES)
def test_abbreviate_name_should_keep_every_portuguese_connector(factory_class):
    assert factory_class.build(full_name="Ana da Silva dos Santos").abbreviate_name() == "Ana da S. dos Santos"


def test_abbreviate_name_breaks_for_users_without_full_name():
    with pytest.raises(AttributeError):
        CoordinationFactory.build().abbreviate_name()
    with pytest.raises(AttributeError):
        GenericUser(email="admin@example.com").abbreviate_name()


def test_str_shows_the_email_for_generic_users():
    assert str(GenericUser(email="admin@example.com")) == "admin@example.com"


@pytest.mark.parametrize("factory_class", NAMED_USER_FACTORIES)
def test_str_shows_the_full_name_for_students_and_advisors(factory_class):
    assert str(factory_class.build(full_name="Maria Lima")) == "Maria Lima"


def test_str_shows_the_code_for_coordinations():
    assert str(CoordinationFactory.build(code="IFPI.THE-ECOMP")) == "IFPI.THE-ECOMP"


def test_code_format_crashes_because_string_upper_does_not_exist():
    with pytest.raises(AttributeError):
        CoordinationFactory.build(code="ifpi.the-ecomp").code_format()


@pytest.mark.xfail(reason="known bug: code_format calls string.upper, which does not exist in Python 3")
def test_code_format_should_return_the_code_in_uppercase():
    assert CoordinationFactory.build(code="ifpi.the-ecomp").code_format() == "IFPI.THE-ECOMP"


def test_email_is_unique_across_roles():
    from django.db import IntegrityError

    StudentFactory(email="same@example.com")
    with pytest.raises(IntegrityError):
        AdvisorFactory(email="same@example.com")


def test_coordination_code_is_unique():
    from django.db import IntegrityError

    CoordinationFactory(code="IFPI.THE-ECOMP")
    with pytest.raises(IntegrityError):
        CoordinationFactory(code="IFPI.THE-ECOMP")
