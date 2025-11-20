from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, UserSession, UserSettings, Game, GameSession
from django.utils import timezone
from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя"""
    user = UserSerializer(read_only=True)
    days_registered = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'games_played', 'last_login_time', 'created_at', 'days_registered']
        read_only_fields = ['id', 'created_at']
    
    def get_days_registered(self, obj):
        """Вычислить количество дней с регистрации"""
        if obj.created_at:
            delta = timezone.now() - obj.created_at
            return delta.days
        return 0


class UserSettingsSerializer(serializers.ModelSerializer):
    """Сериализатор для настроек пользователя"""
    class Meta:
        model = UserSettings
        fields = ['id', 'language', 'theme', 'email_notifications', 
                 'game_notifications', 'news_notifications', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class RegisterSerializer(serializers.Serializer):
    """Сериализатор для регистрации"""
    username = serializers.CharField(max_length=150, min_length=3)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    
    def validate_username(self, value):
        """Валидация имени пользователя"""
        if not value[0].isalpha():
            raise serializers.ValidationError("Имя пользователя должно начинаться с буквы")
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError("Имя пользователя может содержать только буквы, цифры и подчеркивания")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return value
    
    def validate_email(self, value):
        """Валидация email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value
    
    def validate(self, attrs):
        """Валидация совпадения паролей"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        """Создать пользователя"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Профиль и настройки создаются автоматически через сигналы (api/signals.py)
        # Не нужно создавать их вручную, иначе будет ошибка UNIQUE constraint
        
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)
    
    def validate(self, attrs):
        """Валидация и аутентификация"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})
            
            user = authenticate(username=user.username, password=password)
            if not user:
                raise serializers.ValidationError({"password": "Неверный пароль"})
            
            if not user.is_active:
                raise serializers.ValidationError({"email": "Аккаунт деактивирован"})
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Необходимо указать email и пароль")
        
        return attrs


class SessionSerializer(serializers.ModelSerializer):
    """Сериализатор для сессии"""
    user = UserSerializer(read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSession
        fields = ['id', 'session_token', 'user', 'created_at', 'expires_at', 
                 'is_active', 'remember_me', 'is_valid']
        read_only_fields = ['id', 'session_token', 'created_at', 'expires_at']
    
    def get_is_valid(self, obj):
        """Проверить валидность сессии"""
        return obj.is_valid()


class GameSerializer(serializers.ModelSerializer):
    """Сериализатор для игры"""
    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'game_type', 'game_url', 'icon', 'is_active']


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля"""
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, attrs):
        """Валидация"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "Пароли не совпадают"})
        return attrs


class ChangeUsernameSerializer(serializers.Serializer):
    """Сериализатор для смены имени пользователя"""
    new_username = serializers.CharField(max_length=150, min_length=3)
    
    def validate_new_username(self, value):
        """Валидация нового имени пользователя"""
        if not value[0].isalpha():
            raise serializers.ValidationError("Имя пользователя должно начинаться с буквы")
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError("Имя пользователя может содержать только буквы, цифры и подчеркивания")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return value

