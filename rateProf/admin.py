from django.contrib import admin
from .models import Professor, Module, Rating, moduleInstance

admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(moduleInstance)
admin.site.register(Rating)
