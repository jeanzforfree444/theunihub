# Generated by Django 2.2.28 on 2025-03-22 10:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0018_auto_20250312_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polloption',
            name='voted_users',
        ),
        migrations.AddField(
            model_name='poll',
            name='voted_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
