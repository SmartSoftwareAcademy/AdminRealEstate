from django.test import TestCase
from datetime import datetime
from .utils import InvoiceNumberGenerator

class InvoiceNumberGeneratorTestCase(TestCase):
    def setUp(self):
        self.invoice_number_generator = InvoiceNumberGenerator()

    def test_generate_invoice_number(self):
        today = datetime.now()
        year = today.year
        day_of_year = today.timetuple().tm_yday

        # Generate 5 invoice numbers and check if they match the pattern
        for _ in range(5):
            invoice_number = self.invoice_number_generator.generate_invoice_number()
            expected_invoice_number = f"{year}{day_of_year:03d}{self.invoice_number_generator.sequence - 1:08d}"
            self.assertEqual(invoice_number, expected_invoice_number)
