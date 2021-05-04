from django.contrib import admin
from .models import User, District


class UserAdmin(admin.ModelAdmin):
    exclude = ['updated_at']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('updated_at', 'to_time', 'surge_price', 'surge_role', 'minimum_tickets', 'ended')


admin.site.register(User, UserAdmin)
admin.site.register(District, DistrictAdmin)