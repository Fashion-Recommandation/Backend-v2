from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .models import Cloth, Recommendation, Rating
from .serializers import ClothSerializer, RecommendationSerializer, RatingSerializer, UserSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.http import JsonResponse
from core.fashion_recommender import find_suggestions, ComplexLinearRegression
import logging
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from .models import RecommendationRating, UploadedImage

@api_view(['GET'])
def csrf_view(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

def delete_files_in_directory(directory_path):
   try:
     with os.scandir(directory_path) as entries:
       for entry in entries:
         if entry.is_file():
            os.unlink(entry.path)
     print(f"All files in {directory_path} deleted successfully.")
   except OSError:
     print(f"Error occurred while deleting files in {directory_path}.")

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image_view(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    delete_files_in_directory(settings.MEDIA_ROOT)
    delete_files_in_directory(settings.RECOMMENDATIONS_DIR)
    image = request.FILES['image']
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    uploaded_image = UploadedImage(image=image)
    uploaded_image.save()
    uploaded_file_path = uploaded_image.image.path
    print("uploaded_file_path", uploaded_file_path)

    print("this is image:", image, "and this is fs:", fs)
    filename = fs.save(image.name, image)
    upload_path = filename

    print("this is filename name", filename, upload_path)
    # uploaded_file_path = os.path.join(settings.MEDIA_ROOT, filename)
    print("uploaded_file_path", uploaded_file_path)

    clothing_type = request.data.get('clothing_type')
    if clothing_type == 'pants':
        clothing_type = "down"
    else:
        clothing_type = "up"

    recommendations = find_suggestions(uploaded_file_path, clothing_type)
    print("this is test in upload_image_view", image, clothing_type)

    return Response({'message': 'Image uploaded successfully', 'recommendations': recommendations, 'image_path': uploaded_file_path}, status=status.HTTP_201_CREATED)

import os

def find_all_files(directory):
    """Helper function to find all files in a given directory"""
    files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            files.append(filename)
    return files

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def rate_recommendation_view(request):
    name = request.data.get('name')
    age = request.data.get('age')
    gender = request.data.get('gender')
    rating = request.data.get('rating')
    helpful = request.data.get('helpful')
    diverse = request.data.get('diverse')
    usage = request.data.get('usage')
    image = request.data.get('image')
    # suggestions = request.data.get('suggestions')
    min_score_rate = 1
    max_score_rate =10
    
    if None in [name, age, gender, rating, helpful, diverse, usage, image]:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        age = int(age)
        rating = int(rating)
        helpful = int(helpful)
        diverse = int(diverse)
    except ValueError:
        return Response({'error': 'Age, rating, helpful, and diverse must be integers'}, status=status.HTTP_400_BAD_REQUEST)
    
    recommendation_files = find_all_files(settings.RECOMMENDATIONS_DIR)
    recommendations_path = ','.join(recommendation_files) 
    user = request.user
    print("this is filename name2",image)
    recommendation_rating = RecommendationRating(
        name=name,
        age=age,
        gender=gender,
        rating=rating,
        helpful=helpful,
        diverse=diverse,
        usage=usage,
        image=image,
        recommendations_path=recommendations_path
    )
    recommendation_rating.save()
    
    return Response({'message': 'Rating submitted successfully'}, status=status.HTTP_201_CREATED)

def get_cloth_type(image):
    # Implement your logic to determine cloth type from the image
    # This is a placeholder implementation
    return 'shirt' if 'shirt' in image.name.lower() else 'pants'


def get_recommendations(cloth_type):
    # Implement your logic to get recommendations based on cloth type
    # This is a placeholder implementation
    if cloth_type == 'shirt':
        return Recommendation.objects.filter(type='pants')
    else:
        return Recommendation.objects.filter(type='shirt')

def index(request):
    return render(request, 'main/index.html')
