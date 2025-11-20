from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, UserSession, UserSettings, Game, GameSession


class UserProfileInline(admin.StackedInline):
    """Инлайн для профиля пользователя"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профили'
    fk_name = 'user'


class UserSettingsInline(admin.StackedInline):
    """Инлайн для настроек пользователя"""
    model = UserSettings
    can_delete = False
    verbose_name_plural = 'Настройки'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    """Расширенный админ для пользователей"""
    inlines = (UserProfileInline, UserSettingsInline)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Админ для профилей пользователей"""
    list_display = ['user', 'games_played', 'last_login_time', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Статистика', {
            'fields': ('games_played', 'last_login_time', 'created_at')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Админ для сессий пользователей"""
    list_display = ['user', 'session_token_short', 'created_at', 'expires_at', 'is_active', 'remember_me']
    list_filter = ['is_active', 'remember_me', 'created_at']
    search_fields = ['user__username', 'user__email', 'session_token']
    readonly_fields = ['session_token', 'created_at', 'expires_at']
    
    def session_token_short(self, obj):
        """Короткая версия токена"""
        return f"{obj.session_token[:16]}..." if obj.session_token else "-"
    session_token_short.short_description = 'Токен сессии'
    
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Сессия', {
            'fields': ('session_token', 'created_at', 'expires_at', 'remember_me')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )
    
    actions = ['deactivate_sessions']
    
    def deactivate_sessions(self, request, queryset):
        """Деактивировать выбранные сессии"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} сессий деактивировано.')
    deactivate_sessions.short_description = 'Деактивировать выбранные сессии'


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    """Админ для настроек пользователей"""
    list_display = ['user', 'language', 'theme', 'email_notifications', 'game_notifications', 'news_notifications', 'updated_at']
    list_filter = ['language', 'theme', 'email_notifications', 'game_notifications', 'news_notifications']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Интерфейс', {
            'fields': ('language', 'theme')
        }),
        ('Уведомления', {
            'fields': ('email_notifications', 'game_notifications', 'news_notifications')
        }),
        ('Метаданные', {
            'fields': ('updated_at',)
        }),
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Админ для игр"""
    list_display = ['name', 'game_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'game_type', 'created_at']
    search_fields = ['name', 'description', 'game_type']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'game_type')
        }),
        ('Ссылки и иконки', {
            'fields': ('game_url', 'icon')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ['created_at']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    """Админ для сессий игр"""
    list_display = ['user', 'game', 'started_at', 'ended_at', 'duration_display']
    list_filter = ['started_at', 'game']
    search_fields = ['user__username', 'user__email', 'game__name']
    readonly_fields = ['started_at']
    
    def duration_display(self, obj):
        """Отображение длительности"""
        if obj.duration_seconds:
            hours = obj.duration_seconds // 3600
            minutes = (obj.duration_seconds % 3600) // 60
            seconds = obj.duration_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "-"
    duration_display.short_description = 'Длительность'
    
    fieldsets = (
        ('Пользователь и игра', {
            'fields': ('user', 'game')
        }),
        ('Время', {
            'fields': ('started_at', 'ended_at', 'duration_seconds')
        }),
    )


# Перерегистрируем UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Настройка админ-панели
admin.site.site_header = "NDN Store - Администрирование"
admin.site.site_title = "NDN Store Admin"
admin.site.index_title = "Панель управления"
