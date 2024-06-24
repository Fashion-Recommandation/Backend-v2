from rest_framework import serializers
from .models import Cloth, Recommendation, Rating, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ('id', 'user', 'image', 'uploaded_at')
        read_only_fields = ('user',)

    def create(self, validated_data):
        return Cloth.objects.create(**validated_data)

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('id', 'type', 'description')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'recommendation', 'rating')
        read_only_fields = ('user',)
