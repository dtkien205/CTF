from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .models import Game, Level, Employee, Role, Scoreboard, Release
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from .serializers import GameSerializer, LevelSerializer, EmployeeSerializer, RoleSerializer, UserSerializer, ScoreboardSerializer, ReleaseSerializer

class GameView(APIView):
    def post(self, request: Request, format=None):
        try:
            games = Game.objects.filter(is_secret=False, **request.data)
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    def get(self, request: Request, format=None):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LevelListView(APIView):
    def get(self, request: Request, format=None):
        try:
            levels = Level.objects.all()
            serializer = LevelSerializer(levels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ScoreboardView(APIView):
    def get(self, request: Request, format=None):
        try:
            scoreboard = Scoreboard.objects.all()
            serializer = ScoreboardSerializer(scoreboard, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReleaseListView(APIView):
    def get(self, request: Request, format=None):
        try:
            releases = Release.objects.all()
            serializer = ReleaseSerializer(releases, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
