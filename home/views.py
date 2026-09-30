from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import EmployeeForm, MonthlyResultForm, ProductForm
from .models import Employee, MonthlyResult, Product

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
    forms_by_action = {
        'product': ProductForm,
        'result': MonthlyResultForm,
        'employee': EmployeeForm,
    }
    forms = {action: form_class() for action, form_class in forms_by_action.items()}

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action in forms_by_action:
            form = forms_by_action[action](request.POST)
            if form.is_valid():
                record = form.save(commit=False)
                record.owner = request.user
                record.save()
                messages.success(request, 'Registro adicionado.')
                return redirect('dashboard')
            forms[action] = form
        elif action in {'delete_product', 'delete_result', 'delete_employee'}:
            model = {
                'delete_product': Product,
                'delete_result': MonthlyResult,
                'delete_employee': Employee,
            }[action]
            record = get_object_or_404(model, pk=request.POST.get('record_id'), owner=request.user)
            record.delete()
            messages.success(request, 'Registro excluído.')
            return redirect('dashboard')

    context = {
        'products': Product.objects.filter(owner=request.user),
        'results': MonthlyResult.objects.filter(owner=request.user),
        'employees': Employee.objects.filter(owner=request.user),
        'product_form': forms['product'],
        'result_form': forms['result'],
        'employee_form': forms['employee'],
    }
    return render(request, 'core/dashboard.html', context)


@login_required(login_url='auth')
def manage_accounts(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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
            messages.success(request, f'A conta {account.username} foi bloqueada.')
        elif action == 'activate_account':
            account.is_active = True
            account.save(update_fields=['is_active'])
            messages.success(request, f'A conta {account.username} foi reativada.')
        elif action == 'delete_account':
            username = account.username
            account.delete()
            messages.success(request, f'A conta {username} foi excluída.')
        else:
            raise PermissionDenied

        return redirect('manage_accounts')

    accounts = User.objects.filter(is_superuser=False).order_by('username')
    return render(request, 'core/manage_accounts.html', {'accounts': accounts})