# Generated by Django 4.1.1 on 2022-09-29 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cat_image',
            new_name='image',
        ),
    ]
