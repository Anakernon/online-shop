# Generated by Django 4.1 on 2022-08-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_advertisment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisment',
            name='link1',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='advertisment',
            name='link2',
            field=models.URLField(),
        ),
    ]
