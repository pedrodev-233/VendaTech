from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
	name = models.CharField(max_length=120)
	value = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name


class MonthlyResult(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_results')
	month = models.DateField()
	expenses = models.DecimalField(max_digits=12, decimal_places=2)
	profit = models.DecimalField(max_digits=12, decimal_places=2)

	def __str__(self):
		return self.month.strftime('%m/%Y')


class Employee(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employees')
	name = models.CharField(max_length=120)
	role = models.CharField(max_length=100)
	salary = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name


class SalesRecord(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_records')
	product = models.ForeignKey(Product, on_delete=models.CASCADE) # O Produto só pode ser vendido se estiver na tabela de produtos.
	quantity = models.PositiveIntegerField()
	method_of_payment = models.CharField(max_length=50)
	sale_date = models.DateField()

	def __str__(self):
		return self.product.name
