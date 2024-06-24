from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')  # Adjust the upload path as needed
    uploaded_at = models.DateTimeField(auto_now_add=True)

class RecommendationRating(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    rating = models.PositiveIntegerField()
    helpful = models.PositiveIntegerField()
    diverse = models.PositiveIntegerField()
    usage = models.CharField(max_length=10)
    # image = models.ImageField(upload_to='uploaded_images/')  # Adjust the upload path as needed
    image = models.TextField()
    recommendations_path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.rating}'

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

class Cloth(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='clothes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Recommendation(models.Model):
    type = models.CharField(max_length=10)  # 'pants' or 'shirt'
    description = models.TextField()

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
