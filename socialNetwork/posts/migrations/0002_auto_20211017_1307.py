# Generated by Django 3.1.6 on 2021-10-17 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_name',
            new_name='author',
        ),
    ]
