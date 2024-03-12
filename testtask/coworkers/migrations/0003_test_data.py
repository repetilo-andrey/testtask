import random
from datetime import datetime, timedelta

from django.db import migrations

from django_seed import Seed as DjangoSeed

from coworkers.models import Coworker


# Fix Seed Class language issue without changes in library
class Seed(DjangoSeed):
    @classmethod
    def faker(cls, locale=None, codename=None):
        code = codename or cls.codename(locale)
        if code not in cls.fakers:
            from faker import Faker
            cls.fakers[code] = Faker(code)
            cls.fakers[code].seed_instance(random.randint(1, 10000))
        return cls.fakers[code]


end_date = datetime.today()
start_date = end_date - timedelta(days=365)
seeder = Seed.seeder(locale='uk_UA')


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def get_coworkers_data():
    return {
        'start_date': random_date(start_date, end_date),
        'pib': seeder.faker.name(),
        'position': seeder.faker.text(19),
        'email': seeder.faker.email(),
    }


def generate_coworkers(parent=None, level=1, max_levels=7):
    if level >= max_levels:
        return
    num_children = level
    new_coworkers = []
    for i in range(num_children):
        coworkers_data = get_coworkers_data()
        new_coworkers.append(Coworker.objects.create(**coworkers_data, parent=parent))
    for coworker in new_coworkers:
        generate_coworkers(parent=coworker, level=level + 1, max_levels=max_levels)


def generate_root_coworkers(count):
    root_coworkers = []
    for i in range(count):
        root_coworkers.append(Coworker.objects.create(**get_coworkers_data()))
    return root_coworkers


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0002_rename_headman_coworker_parent_coworker_level_and_more'),
    ]

    def insert_data(apps, schema_editor):
        for root_coworker in generate_root_coworkers(60):
            generate_coworkers(parent=root_coworker)

    def reverse_func(apps, schema_editor):
        pass

    operations = [
        migrations.RunPython(insert_data, reverse_func),
    ]
