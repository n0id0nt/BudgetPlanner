from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Report, Item, Prediction, Actual

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(Item)
admin.site.register(Prediction)
admin.site.register(Actual)
