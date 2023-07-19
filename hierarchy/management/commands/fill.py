from random import choice
from faker import Faker
from django.core.management.base import BaseCommand

from home.models import Employee

fake = Faker()

positions = ['System Architect', 'PM', 'Team Lead', "Software Engineer", "HR", "CTO", "Trainee Software Engineer"]


class Command(BaseCommand):
    help = 'Seed the database with fake employee data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of employees to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for _ in range(total):
            full_name = fake.name()
            position = choice(positions)
            email = fake.email()
            hire_date = fake.date()
            manager = Employee.objects.order_by('?').first()
            Employee.objects.create(full_name=full_name, position=position, email=email, manager=manager,
                                    hire_date=hire_date)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total} employees'))
