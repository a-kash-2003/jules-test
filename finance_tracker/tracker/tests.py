from django.test import TestCase
from django.urls import reverse
from .models import Transaction
import datetime

class TransactionModelTest(TestCase):
    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            date=datetime.date.today(),
            description='Test transaction',
            amount=100.00,
            category='Test'
        )
        self.assertEqual(transaction.description, 'Test transaction')

class TransactionViewTest(TestCase):
    def setUp(self):
        self.transaction = Transaction.objects.create(
            date=datetime.date.today(),
            description='Test transaction',
            amount=100.00,
            category='Test'
        )

    def test_transaction_list_view(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test transaction')

    def test_transaction_create_view(self):
        response = self.client.post(reverse('transaction_create'), {
            'date': datetime.date.today(),
            'description': 'New transaction',
            'amount': 50.00,
            'category': 'New'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(description='New transaction').exists())

    def test_transaction_update_view(self):
        response = self.client.post(reverse('transaction_update', args=[self.transaction.pk]), {
            'date': self.transaction.date,
            'description': 'Updated transaction',
            'amount': self.transaction.amount,
            'category': self.transaction.category
        })
        self.assertEqual(response.status_code, 302)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.description, 'Updated transaction')

    def test_transaction_delete_view(self):
        response = self.client.post(reverse('transaction_delete', args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(pk=self.transaction.pk).exists())
