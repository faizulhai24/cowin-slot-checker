from django.contrib import admin
from .models import User, District


class UserAdmin(admin.ModelAdmin):
    exclude = ['updated_at']


class DistrictAdmin(admin.ModelAdmin):
    exclude = ['updated_at']


admin.site.register(User, UserAdmin)
admin.site.register(District, DistrictAdmin)