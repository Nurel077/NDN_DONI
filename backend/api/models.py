from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets


class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    games_played = models.IntegerField(default=0)
    last_login_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"Профиль {self.user.username}"


class UserSession(models.Model):
    """Сессии пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    remember_me = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'Сессия пользователя'
        verbose_name_plural = 'Сессии пользователей'
        indexes = [
            models.Index(fields=['session_token']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"Сессия {self.user.username} - {self.session_token[:8]}"
    
    @classmethod
    def create_session(cls, user, remember_me=False):
        """Создать новую сессию"""
        token = secrets.token_urlsafe(32)
        expires_days = 30 if remember_me else 1
        expires_at = timezone.now() + timedelta(days=expires_days)
        
        session = cls.objects.create(
            user=user,
            session_token=token,
            expires_at=expires_at,
            remember_me=remember_me
        )
        return session
    
    def is_valid(self):
        """Проверить валидность сессии"""
        return self.is_active and timezone.now() < self.expires_at
    
    def deactivate(self):
        """Деактивировать сессию"""
        self.is_active = False
        self.save()


class UserSettings(models.Model):
    """Настройки пользователя"""
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]
    
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Темная'),
        ('auto', 'Авто'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    email_notifications = models.BooleanField(default=True)
    game_notifications = models.BooleanField(default=True)
    news_notifications = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_settings'
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'
    
    def __str__(self):
        return f"Настройки {self.user.username}"


class Game(models.Model):
    """Игры в магазине"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    game_type = models.CharField(max_length=50)  # space, medieval, racing, blast
    game_url = models.URLField()
    icon = models.CharField(max_length=100, blank=True)  # FontAwesome icon class
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'games'
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
    
    def __str__(self):
        return self.name


class GameSession(models.Model):
    """Сессии игр пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'game_sessions'
        verbose_name = 'Сессия игры'
        verbose_name_plural = 'Сессии игр'
        indexes = [
            models.Index(fields=['user', 'started_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.game.name}"
