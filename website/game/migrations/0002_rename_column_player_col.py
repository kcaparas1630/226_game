# Generated by Django 3.2.12 on 2023-11-15 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='column',
            new_name='col',
        ),
    ]