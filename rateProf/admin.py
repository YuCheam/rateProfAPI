from django.contrib import admin
from .models import Professor, Module, User, Rating

admin.site.register(Professor)
admin.site.register(Module)
#admin.site.register(Prof_Module)
admin.site.register(User)
admin.site.register(Rating)
