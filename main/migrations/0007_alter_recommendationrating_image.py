# Generated by Django 5.0.6 on 2024-06-12 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_uploadedimage_alter_recommendationrating_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recommendationrating",
            name="image",
            field=models.ImageField(upload_to="uploaded_images/"),
        ),
    ]
