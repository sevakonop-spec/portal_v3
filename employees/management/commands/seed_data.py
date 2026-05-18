from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import Department, EmployeeProfile


DEPARTMENTS = [
    {'name': 'Executive Office', 'parent': None, 'description': 'Company leadership'},
    {'name': 'Engineering', 'parent': None, 'description': 'Product development'},
    {'name': 'Backend', 'parent': 'Engineering', 'description': 'Server-side systems'},
    {'name': 'Frontend', 'parent': 'Engineering', 'description': 'UI/UX development'},
    {'name': 'DevOps', 'parent': 'Engineering', 'description': 'Infrastructure & CI/CD'},
    {'name': 'Human Resources', 'parent': None, 'description': 'People operations'},
    {'name': 'Finance', 'parent': None, 'description': 'Accounting & planning'},
    {'name': 'Sales', 'parent': None, 'description': 'Revenue & partnerships'},
]

EMPLOYEES = [
    {'username': 'admin',      'first': 'Alice',   'last': 'Anderson', 'email': 'alice@corp.example', 'dept': 'Executive Office', 'title': 'CEO',               'manager': True,  'phone': '+1 555 000 0001', 'is_staff': True, 'is_superuser': True},
    {'username': 'bob',        'first': 'Bob',     'last': 'Baker',    'email': 'bob@corp.example',   'dept': 'Engineering',      'title': 'VP of Engineering',  'manager': True,  'phone': '+1 555 000 0002'},
    {'username': 'carol',      'first': 'Carol',   'last': 'Clark',    'email': 'carol@corp.example', 'dept': 'Backend',          'title': 'Senior Backend Dev', 'manager': True,  'phone': '+1 555 000 0003'},
    {'username': 'dave',       'first': 'Dave',    'last': 'Davis',    'email': 'dave@corp.example',  'dept': 'Backend',          'title': 'Backend Developer',  'phone': '+1 555 000 0004'},
    {'username': 'eve',        'first': 'Eve',     'last': 'Evans',    'email': 'eve@corp.example',   'dept': 'Frontend',         'title': 'Lead Frontend Dev',  'manager': True,  'phone': '+1 555 000 0005'},
    {'username': 'frank',      'first': 'Frank',   'last': 'Foster',   'email': 'frank@corp.example', 'dept': 'Frontend',         'title': 'Frontend Developer', 'phone': '+1 555 000 0006'},
    {'username': 'grace',      'first': 'Grace',   'last': 'Green',    'email': 'grace@corp.example', 'dept': 'DevOps',           'title': 'DevOps Engineer',    'manager': True,  'phone': '+1 555 000 0007'},
    {'username': 'henry',      'first': 'Henry',   'last': 'Hill',     'email': 'henry@corp.example', 'dept': 'Human Resources',  'title': 'HR Manager',         'manager': True,  'phone': '+1 555 000 0008'},
    {'username': 'iris',       'first': 'Iris',    'last': 'Irving',   'email': 'iris@corp.example',  'dept': 'Human Resources',  'title': 'HR Specialist',      'phone': '+1 555 000 0009'},
    {'username': 'jack',       'first': 'Jack',    'last': 'Jones',    'email': 'jack@corp.example',  'dept': 'Finance',          'title': 'CFO',                'manager': True,  'phone': '+1 555 000 0010'},
    {'username': 'kate',       'first': 'Kate',    'last': 'King',     'email': 'kate@corp.example',  'dept': 'Finance',          'title': 'Accountant',         'phone': '+1 555 000 0011'},
    {'username': 'liam',       'first': 'Liam',    'last': 'Lewis',    'email': 'liam@corp.example',  'dept': 'Sales',            'title': 'Sales Manager',      'manager': True,  'phone': '+1 555 000 0012'},
    {'username': 'mia',        'first': 'Mia',     'last': 'Moore',    'email': 'mia@corp.example',   'dept': 'Sales',            'title': 'Account Executive',  'phone': '+1 555 000 0013'},
]


class Command(BaseCommand):
    help = 'Seed the database with sample departments and employees'

    def handle(self, *args, **options):
        dept_map = {}
        for d in DEPARTMENTS:
            parent = dept_map.get(d['parent']) if d['parent'] else None
            dept, created = Department.objects.get_or_create(
                name=d['name'],
                defaults={'parent': parent, 'description': d.get('description', '')}
            )
            dept_map[d['name']] = dept
            self.stdout.write(f"  {'Created' if created else 'Exists '} dept: {dept.name}")

        for e in EMPLOYEES:
            user, created = User.objects.get_or_create(
                username=e['username'],
                defaults={
                    'first_name': e['first'],
                    'last_name': e['last'],
                    'email': e['email'],
                    'is_staff': e.get('is_staff', False),
                    'is_superuser': e.get('is_superuser', False),
                }
            )
            if created:
                user.set_password('password123')
                user.save()

            profile, _ = EmployeeProfile.objects.get_or_create(user=user)
            profile.department = dept_map.get(e['dept'])
            profile.job_title = e.get('title', '')
            profile.phone = e.get('phone', '')
            profile.is_manager = e.get('manager', False)
            profile.save()
            self.stdout.write(f"  {'Created' if created else 'Exists '} user:  {user.get_full_name()} ({user.username})")

        self.stdout.write(self.style.SUCCESS('\nSeed complete. All passwords: password123'))
        self.stdout.write(self.style.SUCCESS('Admin login: admin / password123'))