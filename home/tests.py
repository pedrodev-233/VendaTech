from django.contrib.auth.models import User
from django.test import TestCase

from django.contrib.auth.models import User
from .models import SalesRecord, Product

class SalesRecordTest(TestCase):
    def test_sales_record_creation(self):
        user = User.objects.create_user(username='admin@gmail.com',
                                         password='admin123')

        product = Product.objects.create(owner=user,
                                          name='Hamburguer',
                                          value=20.00)

        sales = SalesRecord.objects.create(owner=user,
                                            product=product,
                                            quantity=2,
                                            method_of_payment='Dinheiro',
                                            sale_date='2023-07-01')

        self.assertEqual(sales.owner, user)
        self.assertEqual(sales.product, product)