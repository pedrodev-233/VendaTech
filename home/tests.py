from django.contrib.auth.models import User
from django.test import TestCase

from .models import Employee, MonthlyResult, Product


class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='dashboard@example.com',
            password='test-password',
        )
        self.client.force_login(self.user)

    def test_dashboard_shows_only_the_logged_in_users_records(self):
        Product.objects.create(owner=self.user, name='Meu produto', value='12.50')
        other_user = User.objects.create_user(
            username='other@example.com',
            password='test-password',
        )
        Product.objects.create(owner=other_user, name='Outro produto', value='20.00')

        response = self.client.get('/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products'].values_list('name', flat=True)), ['Meu produto'])
        self.assertContains(response, 'Nome do produto')
        self.assertNotContains(response, 'Outro produto')

    def test_dashboard_creates_product_from_posted_values(self):
        response = self.client.post('/dashboard/', {
            'action': 'product',
            'name': 'Teclado',
            'value': '149.90',
        })

        self.assertRedirects(response, '/dashboard/')
        self.assertTrue(Product.objects.filter(
            owner=self.user,
            name='Teclado',
            value='149.90',
        ).exists())

    def test_dashboard_creates_monthly_result_from_posted_values(self):
        response = self.client.post('/dashboard/', {
            'action': 'result',
            'month': '2026-10-01',
            'expenses': '400.00',
            'profit': '950.00',
        })

        self.assertRedirects(response, '/dashboard/')
        self.assertTrue(MonthlyResult.objects.filter(
            owner=self.user,
            month='2026-10-01',
            expenses='400.00',
            profit='950.00',
        ).exists())

    def test_dashboard_creates_employee_from_posted_values(self):
        response = self.client.post('/dashboard/', {
            'action': 'employee',
            'name': 'Ana',
            'role': 'Vendedora',
            'salary': '2500.00',
        })

        self.assertRedirects(response, '/dashboard/')
        self.assertTrue(Employee.objects.filter(
            owner=self.user,
            name='Ana',
            role='Vendedora',
            salary='2500.00',
        ).exists())

    def test_dashboard_cannot_delete_another_users_record(self):
        other_user = User.objects.create_user(
            username='other@example.com',
            password='test-password',
        )
        product = Product.objects.create(
            owner=other_user,
            name='Produto alheio',
            value='20.00',
        )

        response = self.client.post('/dashboard/', {
            'action': 'delete_product',
            'record_id': product.pk,
        })

        self.assertRedirects(response, '/dashboard/')
        self.assertTrue(Product.objects.filter(pk=product.pk).exists())