# Generated by Django 4.2.3 on 2023-07-26 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevator', '0003_elevatorrequest_total_floors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elevatorrequest',
            name='total_floors',
        ),
        migrations.AddField(
            model_name='elevator',
            name='total_floors',
            field=models.PositiveIntegerField(default=3),
        ),
    ]
