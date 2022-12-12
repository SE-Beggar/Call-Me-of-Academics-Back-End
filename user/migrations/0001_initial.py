# Generated by Django 3.2.5 on 2022-12-11 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=20, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('sex', models.CharField(max_length=5)),
            ],
        ),
    ]
