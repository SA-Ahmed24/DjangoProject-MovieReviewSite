# Generated by Django 5.0.6 on 2024-06-21 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_movies_featured_image'),
        ('users', '0003_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
    ]
