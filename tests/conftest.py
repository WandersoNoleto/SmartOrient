import pytest
from django.contrib.auth.models import Group

from tests.factories import AdvisorFactory, CoordinationFactory, StudentFactory

ROLE_GROUPS = ("Students", "Advisors", "Coordinations")


@pytest.fixture(autouse=True)
def media_root(tmp_path, settings):
    """Keeps uploaded files out of the project's media/ folder."""
    settings.MEDIA_ROOT = tmp_path / "media"
    return settings.MEDIA_ROOT


@pytest.fixture
def role_groups(db):
    """The role groups the register views expect. No migration creates them (known bug)."""
    return [Group.objects.get_or_create(name=name)[0] for name in ROLE_GROUPS]


@pytest.fixture
def student(db):
    return StudentFactory()


@pytest.fixture
def advisor(db):
    return AdvisorFactory()


@pytest.fixture
def coordination(db):
    return CoordinationFactory()


@pytest.fixture
def student_client(client, student):
    client.force_login(student)
    return client


@pytest.fixture
def advisor_client(client, advisor):
    client.force_login(advisor)
    return client


@pytest.fixture
def coordination_client(client, coordination):
    client.force_login(coordination)
    return client
