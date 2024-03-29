# Generated by Django 5.0.3 on 2024-03-10 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coworker',
            old_name='headman',
            new_name='parent',
        ),
        migrations.AddField(
            model_name='coworker',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coworker',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coworker',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coworker',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coworker',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
