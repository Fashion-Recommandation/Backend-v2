# Generated by Django 5.0.6 on 2024-06-12 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_recommendationrating_gender_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recommendationrating",
            name="recommendations_path",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
