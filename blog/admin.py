from django.contrib import admin
from .models import Person, Image, Chat, Box
# Register your models here.
L = [Person, Image, Chat, Box]
admin.site.register(L)
