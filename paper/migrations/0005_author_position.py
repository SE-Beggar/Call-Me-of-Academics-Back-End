# Generated by Django 3.2.5 on 2022-12-12 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0004_auto_20221211_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='position',
            field=models.CharField(default='', max_length=10),
        ),
    ]
