# Generated by Django 4.0.3 on 2022-03-11 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prize',
            old_name='decription',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='promotion',
            old_name='decription',
            new_name='description',
        ),
    ]