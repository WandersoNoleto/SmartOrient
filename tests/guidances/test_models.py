import datetime
import string

import pytest
from django.db import IntegrityError

from guidances import models as guidance_models
from guidances.models import Guidance
from tests.factories import CoordinationFactory, GuidanceFactory, StudentFactory

pytestmark = pytest.mark.django_db

CODE_CHARS = set(string.ascii_uppercase + string.digits)


@pytest.mark.parametrize(
    ("length", "expected_suffix"),
    [(10, ""), (63, ""), (65, "..."), (150, "...")],
)
def test_project_title_format_truncates_long_titles_to_64_chars(length, expected_suffix):
    title = "x" * length

    formatted = GuidanceFactory.build(project_title=title).project_title_format()

    assert formatted == (title[:64] + expected_suffix if expected_suffix else title)


def test_project_title_format_adds_an_ellipsis_to_titles_with_exactly_64_chars():
    title = "x" * 64

    assert GuidanceFactory.build(project_title=title).project_title_format() == title + "..."


@pytest.mark.xfail(reason="known bug: uses >= instead of >, so a title that fits gets '...'")
def test_project_title_format_should_keep_titles_with_exactly_64_chars():
    title = "x" * 64

    assert GuidanceFactory.build(project_title=title).project_title_format() == title


def test_save_generates_a_six_char_code_once():
    guidance = GuidanceFactory()
    code = guidance.guidance_code

    guidance.save()

    assert len(code) == 6
    assert set(code) <= CODE_CHARS
    assert guidance.guidance_code == code


def test_save_keeps_a_code_that_was_already_set():
    assert GuidanceFactory(guidance_code="ABC123").guidance_code == "ABC123"


def test_generate_guidance_code_retries_until_the_code_is_free(monkeypatch):
    GuidanceFactory(guidance_code="AAAAAA")
    draws = iter(["AAAAAA", "BBBBBB"])
    monkeypatch.setattr(guidance_models.random, "choices", lambda population, k: list(next(draws)))

    guidance = GuidanceFactory.build()

    assert guidance.generate_guidance_code() == "BBBBBB"
    assert guidance.guidance_code == "BBBBBB"


def test_guidance_code_is_unique():
    GuidanceFactory(guidance_code="ABC123")

    with pytest.raises(IntegrityError):
        GuidanceFactory(guidance_code="ABC123")


def test_new_guidances_start_as_pending():
    assert GuidanceFactory().status == "Pendente"


def test_set_start_date_stores_today_as_a_string():
    guidance = GuidanceFactory.build(start_date=None)

    guidance.set_start_date()

    assert guidance.start_date == datetime.date.today().isoformat()


def test_str_is_the_guidance_code():
    assert str(GuidanceFactory.build(guidance_code="ABC123")) == "ABC123"


def test_deleting_the_student_deletes_the_guidance():
    guidance = GuidanceFactory()

    guidance.student.delete()

    assert not Guidance.objects.filter(pk=guidance.pk).exists()


def test_deleting_the_coordination_keeps_the_guidance_without_coordination():
    guidance = GuidanceFactory(coordination=CoordinationFactory())

    guidance.coordination.delete()
    guidance.refresh_from_db()

    assert guidance.coordination is None


def test_student_and_advisor_are_required():
    with pytest.raises(IntegrityError):
        Guidance.objects.create(project_title="Sem orientador", student=StudentFactory(), start_date="2026-11-13")
