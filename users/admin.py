from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'country')
    fields = ('email', 'username', 'avatar', 'phone_number', 'country')