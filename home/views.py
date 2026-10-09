from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProductSerializer, MonthlyResultSerializer, EmployeeSerializer, SalesRecordSerializer
import requests

from .models import Employee, MonthlyResult, Product, SalesRecord

# Create your views here.
def index(request):
    print('Servidor iniciado com sucesso!')
    
    return render(request, 'core/index.html')

def auth(request):
    email = ''
    password = ''   

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('manage_accounts')
            return redirect('dashboard')
        else:
            return render(request, 'core/auth.html', {'error': 'Credenciais inválidas. Tente novamente.'})
    
    return render(request, 'core/auth.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verifica se o email já está cadastrado
        if User.objects.filter(username=email).exists():
            return render(request, 'core/register.html', {
                'error': 'Este email já está cadastrado.'
            })

        # Cria o usuário
        new_user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Faz login automaticamente
        login(request, new_user)

        return redirect('dashboard')

    return render(request, 'core/register.html')

@login_required(login_url='auth')
def dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')


        # Ações de criar registros:
        if action == 'product':
            Product.objects.create(
                owner=request.user,
                name=request.POST.get('name'),
                value=request.POST.get('value')
            )

        elif action == 'result':
            MonthlyResult.objects.create(
                owner=request.user,
                month=request.POST.get('month'),
                expenses=request.POST.get('expenses'),
                profit=request.POST.get('profit')
            )

        elif action == 'employee':
            Employee.objects.create(
                owner=request.user,
                name=request.POST.get('name'),
                role=request.POST.get('role'),
                salary=request.POST.get('salary')
            )

        elif action == 'sale':
            SalesRecord.objects.create(
                owner=request.user,
                product_id=request.POST.get('product'),
                quantity=request.POST.get('quantity'),
                method_of_payment=request.POST.get('method_of_payment'),
                sale_date=request.POST.get('sale_date')
            )


        # Ações de deletar registros:
        if action == 'delete_product':
            Product.objects.filter(
                id=request.POST.get('record_id'),
                owner=request.user
            ).delete()

        elif action == 'delete_result': 
            MonthlyResult.objects.filter(
                id=request.POST.get('record_id'),
                owner=request.user
            ).delete()

        elif action == 'delete_employee':
            Employee.objects.filter(
                id=request.POST.get('record_id'),
                owner=request.user
            ).delete()

        return redirect('dashboard')

    context = {
        'products': Product.objects.filter(owner=request.user),
        'results': MonthlyResult.objects.filter(owner=request.user),
        'employees': Employee.objects.filter(owner=request.user),
        'sales': SalesRecord.objects.filter(owner=request.user),
    }

    return render(request, 'core/dashboard.html', context)


@login_required(login_url='auth')
def page_report(request):
    
    return render(request, 'core/report.html')


@login_required(login_url='auth')
def manage_accounts(request):
    if not request.user.is_superuser:
        return redirect('index')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        account = get_object_or_404(
            User,
            pk=request.POST.get('user_id'),
            is_superuser=False,
        )

        if action == 'block_account':
            account.is_active = False
            account.save(update_fields=['is_active'])
            return render(request, f'A conta {account.username} foi bloqueada.')
        elif action == 'activate_account':
            account.is_active = True
            account.save(update_fields=['is_active'])
            return render(request, f'A conta {account.username} foi reativada.')
        elif action == 'delete_account':
            username = account.username
            account.delete()
            return render(request, f'A conta {username} foi excluída.')
        else:
            return render(request, 'core/manage_accounts.html', {'error': 'Ação não permitida.'})

    accounts = User.objects.filter(is_superuser=False).order_by('username')
    return render(request, 'core/manage_accounts.html', {'accounts': accounts})


# APIs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def API_relatorio(request):
    products = ProductSerializer(
        Product.objects.filter(owner=request.user),many=True).data

    results = MonthlyResultSerializer(
        MonthlyResult.objects.filter(owner=request.user), many=True).data

    employees = EmployeeSerializer(
        Employee.objects.filter(owner=request.user), many=True).data

    sales = SalesRecordSerializer(
        SalesRecord.objects.filter(owner=request.user), many=True).data

    dados = {
        'products': products,
        'results': results,
        'employees': employees,
        'sales': sales,
    }
    return Response(dados)
