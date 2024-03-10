import random
from datetime import datetime, timedelta

from django.db import migrations, models

from django_seed import Seed


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


def generate_coworkers(Coworker, parent=None, level=1, max_levels=8):
    if level >= max_levels:
        return
    num_children = random.randint(level * 10, level * 20)
    for i in range(num_children):
        coworkers_data = get_coworkers_data()
        coworkers_data['headman_id'] = parent.id
        coworker = Coworker.objects.create(**coworkers_data, headman=parent)
        generate_coworkers(Coworker, parent=coworker, level=level + 1, max_levels=max_levels)


def generate_root_coworkers(Coworker, count):
    root_coworkers = []
    for i in range(count):
        root_coworkers.append(Coworker.objects.create(**get_coworkers_data()))
    return root_coworkers


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0001_initial'),
    ]

    def insert_data(apps, schema_editor):
        Coworker = apps.get_model('coworkers', 'Coworker')
        for root_coworker in generate_root_coworkers(Coworker, 200):
            generate_coworkers(Coworker, parent=root_coworker)

    def reverse_func(apps, schema_editor):
        pass

    operations = [
        migrations.AlterField(
            model_name='coworker',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.RunPython(insert_data, reverse_func),
    ]
