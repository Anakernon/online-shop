# Generated by Django 4.1 on 2022-08-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_alter_advertisment_link1_alter_advertisment_link2'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisment',
            name='btn1',
            field=models.CharField(default='Button', max_length=32),
        ),
        migrations.AddField(
            model_name='advertisment',
            name='btn2',
            field=models.CharField(default='Button', max_length=32),
        ),
    ]
