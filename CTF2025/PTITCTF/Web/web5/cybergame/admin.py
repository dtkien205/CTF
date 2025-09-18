from django.contrib import admin
from .models import Game, Level, Employee, Role,Scoreboard,Release

admin.site.register(Game)
admin.site.register(Level)
admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Scoreboard)
admin.site.register(Release)