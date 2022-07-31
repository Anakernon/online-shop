# Generated by Django 3.2.14 on 2022-07-31 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20220731_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='menu/static/menu/images/menu'),
        ),
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(upload_to='menu/static/menu/images/menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ImageField(upload_to='menu/static/menu/images/menu'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='menu/static/menu/images/products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(upload_to='menu/static/menu/images/products'),
        ),
    ]