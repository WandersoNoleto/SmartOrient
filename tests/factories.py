import datetime

import factory
from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory

from guidances.models import Guidance
from library.models import GuidanceArticle
from users.models import Advisor, Coordination, Student

PASSWORD = "s3nha-forte"

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[]/Count 0>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF"
)


def role_group(name):
    """Adds the user to its role group. Pass in_role_group=False to skip it."""

    @factory.post_generation
    def in_role_group(obj, create, extracted, **kwargs):
        if create and extracted is not False:
            group, _ = Group.objects.get_or_create(name=name)
            obj.groups.add(group)

    return in_role_group


class RoleUserFactory(DjangoModelFactory):
    """Creates users through the manager, like the register views do."""

    class Meta:
        abstract = True
        skip_postgeneration_save = True  # the hook only touches the M2M, no extra save needed

    password = PASSWORD

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return model_class.objects.create_user(*args, **kwargs)


class StudentFactory(RoleUserFactory):
    class Meta:
        model = Student

    email = factory.Sequence(lambda n: f"student{n}@example.com")
    full_name = factory.Faker("name", locale="pt_BR")
    course = "Engenharia de Computação"
    institution = "IFPI"
    enrollment = factory.Sequence(lambda n: f"2023{n:04d}")
    phone_number = "86999990000"
    in_role_group = role_group("Students")


class AdvisorFactory(RoleUserFactory):
    class Meta:
        model = Advisor

    email = factory.Sequence(lambda n: f"advisor{n}@example.com")
    full_name = factory.Faker("name", locale="pt_BR")
    institution = "IFPI"
    enrollment = factory.Sequence(lambda n: f"P{n:04d}")
    phone_number = "86999990001"
    in_role_group = role_group("Advisors")


class CoordinationFactory(RoleUserFactory):
    class Meta:
        model = Coordination

    email = factory.Sequence(lambda n: f"coordination{n}@example.com")
    course = "Engenharia de Computação"
    institution = "IFPI"
    campus = "THE"
    code = factory.Sequence(lambda n: f"IFPI.THE-C{n}")
    in_role_group = role_group("Coordinations")


class GuidanceFactory(DjangoModelFactory):
    class Meta:
        model = Guidance

    project_title = factory.Faker("sentence", nb_words=8, locale="pt_BR")
    student = factory.SubFactory(StudentFactory)
    advisor = factory.SubFactory(AdvisorFactory)
    coordination = factory.SubFactory(CoordinationFactory)
    start_date = factory.LazyFunction(datetime.date.today)


class GuidanceArticleFactory(DjangoModelFactory):
    class Meta:
        model = GuidanceArticle

    title = factory.Sequence(lambda n: f"Capitulo{n}.pdf")
    file = factory.django.FileField(filename="documento.pdf", data=MINIMAL_PDF)
    guidance = factory.SubFactory(GuidanceFactory, status="Em andamento")
