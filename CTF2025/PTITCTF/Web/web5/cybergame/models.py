from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role, related_name='user')

class Level(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Game(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    levels = models.ManyToManyField(Level, related_name="games")
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_secret = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title}-{self.created_by.user.username}"
    
    class Meta:
        ordering = ["title"]

class Scoreboard(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='scoreboard')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.game.title} - {self.score}"

class Release(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='releases')
    release_date = models.DateField()

    def __str__(self):
        return f"{self.game.title} - {self.release_date}"
