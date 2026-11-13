import datetime

import pytest

from library.models import GuidanceArticle
from tests.factories import GuidanceArticleFactory

pytestmark = pytest.mark.django_db


def test_title_format_drops_the_last_four_chars():
    article = GuidanceArticleFactory.build(title="Capitulo1.pdf")

    article.title_format()

    assert article.title == "Capitulo1"


@pytest.mark.xfail(reason="known bug: title_format cuts 4 chars even when the title has no extension")
def test_title_format_should_keep_titles_without_extension():
    article = GuidanceArticleFactory.build(title="Proposta")

    article.title_format()

    assert article.title == "Proposta"


def test_set_date_uploaded_stores_today_as_a_string():
    article = GuidanceArticleFactory.build()

    article.set_date_uploaded()

    assert article.date_uploaded == datetime.date.today().isoformat()


def test_date_uploaded_is_filled_on_creation():
    assert GuidanceArticleFactory().date_uploaded == datetime.date.today()


def test_files_are_stored_under_guidance_articles():
    assert GuidanceArticleFactory().file.name.startswith("guidance_articles/")


def test_str_is_the_title():
    assert str(GuidanceArticleFactory.build(title="Capitulo1.pdf")) == "Capitulo1.pdf"


def test_deleting_the_guidance_deletes_its_articles():
    article = GuidanceArticleFactory()

    article.guidance.delete()

    assert not GuidanceArticle.objects.filter(pk=article.pk).exists()
