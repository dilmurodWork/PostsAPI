# Session Token 🪙 orqali auntifikatsiyadan o'tish 

1. virtual muhitni yaratamiz 💻
```shell
py -m venv venv 
```
2. virtual muhitni aktivlashtiramiz
```shell
venv\Scripts\activate
```  
3. kerakli kutubxonalarni o'rnatamiz 📚
```shell
pip install djangorestframework
pip install djoser
```
4. django proyekt yaratamiz
```shell
django-admin startproject config .
```
5. proyektimiz uchun app yaratamiz
```shell
py manage.py startapp post
```
6. `settings.py`ni sozlab olamiz:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'post', # new
    'rest_framework', # new
    'rest_framework.authtoken', # new
    'djoser' # new
]

...

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

...

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

```
7.  `post/models.py` ichida modelimizni yaratib olamiz
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

class PostModel(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'
        ordering = ['-created']

    def __str__(self):
        return self.title
```
7.1 Modelimizni yaratgandan so'ng migratisiya hosil qilamiz
```shell
py manage.py makemigrations
```
7.2 So'ngra migratisiya qilamiz
```shell
py manage.py migrate
```
7.3 Super userimizni yaratamiz 
```shell
py manage.py createsuperuser
```
8. `User`ni o'zgartirganimiz sababli `settings.py`ga `AUTH_USER_MODEL = 'post.User'`ni qo'shamiz
```python
AUTH_USER_MODEL = 'post.User'
```


9. `post/serializers.py` yaratib olib quyidagi kodni yozamiz
```python
from rest_framework import serializers
from .models import PostModel


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # user mizni yashirib unga aktiv bo'lgan foydalanuvchini o'rnatish uchun 
    author = serializers.ReadOnlyField(source='user.username')  # avtor maydoni yaratib unga userni qiymatini beramiz get requestda ko'rib turish uchun

    class Meta:
        model = PostModel   
        fields = '__all__'
```
10. O'zmizning premissionlarni o'rnatish uchun  `post/permissions.py`ni yaratamiz
```python
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):                  # foydalanuvchiga permissions berish uchun
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):         # obyektga permissions berish uchun 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

```
11. `post/views.py`
```python
from django.shortcuts import render
from .models import PostModel
from .serializers import PostSerializer
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


class PostAPI(ListCreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
```
12. post/urls.py ni yaratin olamiz
```python
from django.urls import path
from .views import PostAPI, PostDetail

urlpatterns = [
    path('api/v1/posts', PostAPI.as_view()),
    path('api/v1/post/<int:pk>', PostDetail.as_view()),
]
```
13. `config/urls.py`ga `path('', include('post.urls'))`ni yozamiz 
```python
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('post.urls')),  # new
    path('auth-drf', include('rest_framework.urls')), # new 
    re_path(r'^auth/', include('djoser.urls')), # new 
    re_path(r'^auth/', include('djoser.urls.authtoken')), # new
]
```
14. proyektimizni ishga tushuramiz
```shell
py manage.py runserver
```
