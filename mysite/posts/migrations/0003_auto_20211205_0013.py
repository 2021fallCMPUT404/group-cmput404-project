# Generated by Django 3.1.6 on 2021-12-05 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
