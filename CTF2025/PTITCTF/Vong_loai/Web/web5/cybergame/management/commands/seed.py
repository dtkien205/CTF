from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cybergame.models import Role, Employee, Level, Game, Scoreboard, Release
from random import randint, choice
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        # Idempotent guard: skip seeding if users already exist
        if User.objects.exists():
            self.stdout.write('Seed already applied, skipping.')
            return

        role_admin = Role.objects.create(name='Admin')
        role_developer = Role.objects.create(name='Developer')
        
        users = []
        for i in range(1, 11):
            user = User.objects.create_user(
                username=f'user{i}', 
                password=f'password{i}', 
                email=f'user{i}@example.com', 
                first_name=f'First{i}', 
                last_name=f'Last{i}'
            )
            users.append(user)
        
        employees = []
        for i, user in enumerate(users):
            employee = Employee.objects.create(user=user)
            if i % 2 == 0:
                employee.role.add(role_admin)
            else:
                employee.role.add(role_developer)
            employees.append(employee)
        
        levels = []
        for i in range(1, 21):  
            level = Level.objects.create(name=f'Level {i}')
            levels.append(level)
        
        games = []
        for i in range(1, 20):
            if (i%3 == 0):
                game = Game.objects.create(
                    title=f'Game {i}', 
                    body=f'Description of Game {i}', 
                    created_by=choice(employees), 
                    is_secret=True
                )
            elif (i==17):
                game = Game.objects.create(
                    title='Secret Game', 
                    body='flag{F4K3_FL4G}',
                    created_by=choice(employees), 
                    is_secret=True
                    )
            else:
                game = Game.objects.create(
                    title=f'Game {i}', 
                    body=f'Description of Game {i}', 
                    created_by=choice(employees), 
                    is_secret=False
                )
            game.levels.set(choice(levels) for _ in range(randint(1, 5)))
            games.append(game)

        for game in games:
            for user in users:
                Scoreboard.objects.create(
                    game=game, 
                    user=user, 
                    score=randint(0, 1000)  
                )
        
        for game in games:
            release_date = datetime.now().date() - timedelta(days=randint(0, 365))  
            Release.objects.create(
                game=game, 
                release_date=release_date
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
