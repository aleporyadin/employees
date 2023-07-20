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
            managers_pks = Employee.objects.values_list('pk', flat=True)
            manager_pk = choice(managers_pks) if managers_pks else None

            manager = Employee.objects.get(pk=manager_pk) if manager_pk else None

            Employee.objects.create(full_name=full_name, position=position, email=email, manager=manager,
                                    hire_date=hire_date)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total} employees'))
