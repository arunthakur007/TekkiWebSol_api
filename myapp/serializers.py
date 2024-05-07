from rest_framework import serializers
from .models import CustomUser
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        members = UserSerializer(many=True, read_only=True)
        model = Task
        fields = '__all__'

class TaskMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username'] 

class TokenSerializer(serializers.Serializer):
    """
    Serializer for JWT token
    """
    token = serializers.CharField(max_length=255)   