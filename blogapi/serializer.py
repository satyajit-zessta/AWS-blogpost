from rest_framework import serializers
from blogging.models import *
# from django.template.defaultfilters import slugify
# import re


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['id']

    def validate(self, attrs):
        user_name = attrs.get('user_name', '').lower()
        password = attrs.get('password', '')
        email = attrs.get('email', '')

        if User.objects.filter(user_name=user_name).exists():
            raise serializers.ValidationError("Username already exists")

        if len(password) < 4:
            raise serializers.ValidationError({'password': ['Password must be at least 4 characters']})

        if '@' not in email:
            raise serializers.ValidationError('Invalid Email Address')

        if len(user_name) > 30:
            raise serializers.ValidationError('User Name should be less than 30 characters')

        return attrs


    def create(self, validated_data):
        # Override create method to set the password using set_password method
        user = User.objects.create_user(**validated_data)
        return user

        
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer() # Doesn't serialize the 'excluded fields'
    class Meta:
        model = Post
        fields = '__all__'
        # depth = 1 # Serializes all the fields including 'exculded fields'
    
class TagSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many = True)
    class Meta:
        model = Tagging
        fields = '__all__'
        # depth = 2
    

class CommentSerializer(serializers.ModelSerializer):
   # post = PostSerializer(many = True)
    class Meta:
        model = Comment
        fields = '__all__'
        # depth = 1
