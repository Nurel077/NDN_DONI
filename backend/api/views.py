from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import UserProfile, UserSession, UserSettings, Game, GameSession
from .serializers import (
    UserSerializer, UserProfileSerializer, UserSettingsSerializer,
    RegisterSerializer, LoginSerializer, SessionSerializer,
    GameSerializer, ChangePasswordSerializer, ChangeUsernameSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя через Django"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Автоматически логиним пользователя после регистрации
        login(request, user)
        
        # Обновить профиль (профиль создается автоматически через сигналы)
        # Используем get_or_create на всякий случай
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.last_login_time = timezone.now()
        profile.save()
        
        return Response({
            'success': True,
            'message': 'Регистрация успешна',
            'user': UserSerializer(user).data,
            'is_authenticated': request.user.is_authenticated
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Вход пользователя через Django"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        remember_me = serializer.validated_data.get('remember_me', False)
        
        # Логиним пользователя через Django
        login(request, user)
        
        # Настройка длительности сессии
        if remember_me:
            request.session.set_expiry(2592000)  # 30 дней
        else:
            request.session.set_expiry(86400)  # 1 день
        
        # Обновить профиль
        profile = user.profile
        profile.last_login_time = timezone.now()
        profile.save()
        
        return Response({
            'success': True,
            'message': 'Вход выполнен успешно',
            'user': UserSerializer(user).data,
            'is_authenticated': request.user.is_authenticated
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """Выход пользователя через Django"""
    if request.user.is_authenticated:
        logout(request)
        return Response({
            'success': True,
            'message': 'Выход выполнен успешно'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Пользователь не авторизован'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def validate_session(request):
    """Проверка валидности сессии Django"""
    if request.user.is_authenticated:
        return Response({
            'success': True,
            'valid': True,
            'user': UserSerializer(request.user).data,
            'is_authenticated': True
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': True,
        'valid': False,
        'message': 'Пользователь не авторизован',
        'is_authenticated': False
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Получить профиль пользователя через Django"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Пользователь не авторизован'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    profile = request.user.profile
    settings = request.user.settings
    
    return Response({
        'success': True,
        'profile': UserProfileSerializer(profile).data,
        'settings': UserSettingsSerializer(settings).data
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_settings(request):
    """Обновить настройки пользователя через Django"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Пользователь не авторизован'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    settings = request.user.settings
    serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Настройки обновлены',
            'settings': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Изменить пароль через Django"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Пользователь не авторизован'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        current_password = serializer.validated_data['current_password']
        
        if not user.check_password(current_password):
            return Response({
                'success': False,
                'message': 'Неверный текущий пароль'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Обновляем сессию после смены пароля
        login(request, user)
        
        return Response({
            'success': True,
            'message': 'Пароль успешно изменен'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_username(request):
    """Изменить имя пользователя через Django"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Пользователь не авторизован'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = ChangeUsernameSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        user.username = serializer.validated_data['new_username']
        user.save()
        
        return Response({
            'success': True,
            'message': 'Имя пользователя успешно изменено',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Удалить аккаунт через Django"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Пользователь не авторизован'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    user = request.user
    
    # Деактивировать профиль
    profile = user.profile
    profile.is_active = False
    profile.save()
    
    # Деактивировать пользователя
    user.is_active = False
    user.save()
    
    # Выходим из системы
    logout(request)
    
    return Response({
        'success': True,
        'message': 'Аккаунт успешно удален'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_games(request):
    """Получить список игр"""
    games = Game.objects.filter(is_active=True)
    serializer = GameSerializer(games, many=True)
    return Response({
        'success': True,
        'games': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """Получить CSRF токен"""
    from django.middleware.csrf import get_token
    token = get_token(request)
    return Response({
        'csrftoken': token
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_game_session(request):
    """Начать сессию игры через Django"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Пользователь не авторизован'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    game_type = request.data.get('game_type')
    
    if not game_type:
        return Response({
            'success': False,
            'message': 'Не указан тип игры'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        game = Game.objects.get(game_type=game_type, is_active=True)
    except Game.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Игра не найдена'
        }, status=status.HTTP_404_NOT_FOUND)
    
    game_session = GameSession.objects.create(
        user=request.user,
        game=game
    )
    
    # Увеличить счетчик игр
    profile = request.user.profile
    profile.games_played += 1
    profile.save()
    
    return Response({
        'success': True,
        'message': 'Сессия игры начата',
        'game_session_id': game_session.id
    }, status=status.HTTP_201_CREATED)
