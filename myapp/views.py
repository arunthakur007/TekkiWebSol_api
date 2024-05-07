from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, TaskSerializer, TaskMemberSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import Task, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token, RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.tokens import Token, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError



@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            # Generate access and refresh tokens
            try:
                access_token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
            except TokenError as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Serialize tokens
            token_data = {
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
            }

            return Response(token_data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(task, data=request.data, partial=True)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task_member(request, task_id, user_id):
    try:
        task = Task.objects.get(pk=task_id)
        user = CustomUser.objects.get(pk=user_id)
    except (Task.DoesNotExist, CustomUser.DoesNotExist):
        return Response({'error': 'Task or user not found'}, status=status.HTTP_404_NOT_FOUND)
    
    task.members.add(user)
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_task_member(request, task_id, user_id):
    try:
        task = Task.objects.get(pk=task_id)
        user = CustomUser.objects.get(pk=user_id)
    except (Task.DoesNotExist, CustomUser.DoesNotExist):
        return Response({'error': 'Task or user not found'}, status=status.HTTP_404_NOT_FOUND)
    
    task.members.remove(user)
    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    new_status = request.data.get('status')
    if new_status in ['Todo', 'Inprogress', 'Done']:
        task.status = new_status
        task.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
