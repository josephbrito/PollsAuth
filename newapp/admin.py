from django.contrib import admin
from .models import User, Question, Choice


admin.site.register(User)
admin.site.register(Question)
admin.site.register(Choice)

# Register your models here.
