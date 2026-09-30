from django import forms

from .models import Employee, MonthlyResult, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'value']
        labels = {'name': 'Nome do produto', 'value': 'Valor'}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ex.: Café especial'}),
            'value': forms.NumberInput(attrs={'placeholder': '0,00', 'step': '0.01', 'min': '0'}),
        }


class MonthlyResultForm(forms.ModelForm):
    month = forms.DateField(
        input_formats=['%Y-%m'],
        label='Mês',
        widget=forms.DateInput(format='%Y-%m', attrs={'type': 'month'}),
    )

    class Meta:
        model = MonthlyResult
        fields = ['expenses', 'profit', 'month']
        labels = {'expenses': 'Gastos', 'profit': 'Lucro'}
        widgets = {
            'expenses': forms.NumberInput(attrs={'placeholder': '0,00', 'step': '0.01', 'min': '0'}),
            'profit': forms.NumberInput(attrs={'placeholder': '0,00', 'step': '0.01'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'role', 'salary']
        labels = {'name': 'Nome', 'role': 'Cargo', 'salary': 'Salário'}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome do funcionário'}),
            'role': forms.TextInput(attrs={'placeholder': 'Ex.: Vendedor(a)'}),
            'salary': forms.NumberInput(attrs={'placeholder': '0,00', 'step': '0.01', 'min': '0'}),
        }