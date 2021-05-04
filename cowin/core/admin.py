from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ['updated_at']


admin.site.register(User, UserAdmin)
