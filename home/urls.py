from django.urls import path
from .views import index, auth, dashboard, manage_accounts, register, API_relatorio, page_report, politicas, account_settings

urlpatterns = [
    path('', index, name='index'),
    path('auth/', auth, name='auth'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('configuracoes/', account_settings, name='account_settings'),
    path('accounts/', manage_accounts, name='manage_accounts'),
    path('report/', page_report, name='report'),
    path('politica', politicas, name='politica'),
    path('API/report/', API_relatorio, name='API_Relatorio')
]