# Generated by Django 3.2.5 on 2022-12-11 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0002_auto_20221211_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(1, 'Sedan'), (2, 'Truck'), (4, 'SUV')])),
            ],
        ),
    ]
