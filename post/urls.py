from django.urls import path
from .views import PostAPI, PostDetail

urlpatterns = [
    path('api/v1/posts', PostAPI.as_view()),
    path('api/v1/post/<int:pk>', PostDetail.as_view()),
]
