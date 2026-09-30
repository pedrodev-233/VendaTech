from django.urls import path
from .views import index, auth, dashboard, manage_accounts, register

urlpatterns = [
    path('', index, name='index'),
    path('auth/', auth, name='auth'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('contas/', manage_accounts, name='manage_accounts'),
]