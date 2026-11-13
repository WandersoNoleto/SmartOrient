import pytest

from tests.factories import (
    PASSWORD,
    AdvisorFactory,
    CoordinationFactory,
    GuidanceArticleFactory,
    GuidanceFactory,
    StudentFactory,
)

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ("factory_class", "group_name"),
    [
        (StudentFactory, "Students"),
        (AdvisorFactory, "Advisors"),
        (CoordinationFactory, "Coordinations"),
    ],
)
def test_role_user_factories_create_usable_accounts(factory_class, group_name):
    user = factory_class()

    assert user.check_password(PASSWORD)
    assert list(user.groups.values_list("name", flat=True)) == [group_name]


def test_role_user_factory_can_skip_the_group():
    assert not StudentFactory(in_role_group=False).groups.exists()


def test_guidance_factory_builds_a_full_guidance():
    guidance = GuidanceFactory()

    assert guidance.status == "Pendente"
    assert len(guidance.guidance_code) == 6
    assert guidance.coordination is not None


def test_guidance_article_factory_stores_the_file_in_the_temporary_media_root(media_root):
    article = GuidanceArticleFactory()

    assert article.file.path.startswith(str(media_root))
    with article.file.open("rb") as stored:
        assert stored.read().startswith(b"%PDF")
