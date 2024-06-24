from django.urls import path
from .views import index, login_view, register_view, upload_image_view, rate_recommendation_view, csrf_view

urlpatterns = [
    # path('', index, name='index'),
    # path('api/register/', register_view, name='register'),
    # path('api/login/', login_view, name='login'),
    # path('api/upload/', upload_image_view, name='upload_image'),
    # path('api/rate/<int:recommendation_id>/', rate_recommendation_view, name='rate_recommendation'),
    # path('csrf/', csrf_view, name='csrf'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('upload/', upload_image_view, name='upload'),
    path('csrf/', csrf_view, name='csrf'),
    path('rate/', rate_recommendation_view, name='rate_recommendation'),

]
