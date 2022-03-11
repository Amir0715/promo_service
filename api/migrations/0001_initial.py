# Generated by Django 4.0.3 on 2022-03-11 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decription', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.prize')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winners', to='api.participant')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('decription', models.TextField()),
                ('participants', models.ManyToManyField(related_name='promotions', to='api.participant')),
                ('prizes', models.ManyToManyField(related_name='promotions', to='api.prize')),
            ],
        ),
    ]
