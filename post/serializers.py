from rest_framework import serializers
from .models import PostModel


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PostModel
        fields = '__all__'
