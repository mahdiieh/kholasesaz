# Generated by Django 2.2.20 on 2022-02-03 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20220203_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summary',
            name='created',
        ),
    ]
