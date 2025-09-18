from rest_framework import serializers
from .models import Game, Level, Employee, Role, Scoreboard, Release
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'user', 'role')

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('id', 'name')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('title', 'body')

class ScoreboardSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = Scoreboard
        fields = ('id', 'user', 'game', 'score')

class ReleaseSerializer(serializers.ModelSerializer):
    game = GameSerializer()

    class Meta:
        model = Release
        fields = ('id', 'game', 'release_date')
