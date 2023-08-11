import datetime
import random
import string

class InvoiceNumberGenerator:
    def __init__(self):
        self.today = datetime.datetime.now()
        self.year = self.today.year
        self.day_of_year = self.today.timetuple().tm_yday
        self.sequence = 1

    def generate_invoice_number(self):
        invoice_number = f"{self.year}{self.day_of_year:03d}{self.sequence:08d}"
        self.sequence += 1
        return invoice_number

    def generate_random_code(self,length=8):
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(length))
        return code

