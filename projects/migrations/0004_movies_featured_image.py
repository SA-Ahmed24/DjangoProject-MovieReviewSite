# Generated by Django 5.0.6 on 2024-06-20 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_movies_vote_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
