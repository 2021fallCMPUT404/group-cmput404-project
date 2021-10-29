# Generated by Django 3.2.8 on 2021-10-28 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_alter_post_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_created']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='comment_body',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_date',
            new_name='comment_created',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='username',
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post'),
        ),
    ]
