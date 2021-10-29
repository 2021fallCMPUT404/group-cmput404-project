# Generated by Django 3.1.6 on 2021-10-23 17:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211023_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUUIDModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='displayName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='username', to='users.displayname'),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.myuuidmodel'),
        ),
    ]
