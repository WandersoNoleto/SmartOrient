import pytest

from users.models import GenericUser, Student

pytestmark = pytest.mark.django_db


def test_create_user_normalizes_the_email_domain_and_hashes_the_password():
    user = GenericUser.objects.create_user("Maria@EXAMPLE.COM", "s3nha-forte")

    assert user.email == "Maria@example.com"
    assert user.password != "s3nha-forte"
    assert user.check_password("s3nha-forte")
    assert (user.is_active, user.is_staff, user.is_superuser) == (True, False, False)


def test_create_user_passes_extra_fields_to_role_models():
    student = Student.objects.create_user("maria@example.com", "s3nha-forte", full_name="Maria Lima", course="ECOMP")

    assert (student.full_name, student.course) == ("Maria Lima", "ECOMP")
    assert GenericUser.objects.filter(pk=student.pk).exists()


@pytest.mark.parametrize("email", ["", None])
def test_create_user_requires_an_email(email):
    with pytest.raises(ValueError, match="Email must be set"):
        GenericUser.objects.create_user(email, "s3nha-forte")


def test_create_superuser_sets_the_admin_flags():
    admin = GenericUser.objects.create_superuser("admin@example.com", "s3nha-forte")

    assert (admin.is_active, admin.is_staff, admin.is_superuser) == (True, True, True)


@pytest.mark.parametrize("flag", ["is_staff", "is_superuser"])
def test_create_superuser_rejects_disabled_admin_flags(flag):
    with pytest.raises(ValueError, match=f"Superuser must have {flag}=True"):
        GenericUser.objects.create_superuser("admin@example.com", "s3nha-forte", **{flag: False})
