from django.urls import path
from .views import index, auth, dashboard, manage_accounts, register, API_relatorio, page_report

urlpatterns = [
    path('', index, name='index'),
    path('auth/', auth, name='auth'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', manage_accounts, name='manage_accounts'),
    path('report/', page_report, name='report'),
    path('API/relatório/', API_relatorio, name='API_Relatorio')
]