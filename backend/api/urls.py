from django.urls import path
from . import views

urlpatterns = [
    # CSRF токен
    path('csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    
    # Аутентификация (Django)
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('validate-session/', views.validate_session, name='validate_session'),
    
    # Профиль (требует авторизации)
    path('profile/', views.get_profile, name='get_profile'),
    
    # Настройки (требует авторизации)
    path('settings/', views.update_settings, name='update_settings'),
    
    # Управление аккаунтом (требует авторизации)
    path('change-password/', views.change_password, name='change_password'),
    path('change-username/', views.change_username, name='change_username'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    # Игры
    path('games/', views.get_games, name='get_games'),
    path('start-game/', views.start_game_session, name='start_game_session'),
]

