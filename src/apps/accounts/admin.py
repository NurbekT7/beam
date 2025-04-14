from django.contrib import admin
from apps.accounts.models import User

class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Main', {
            'fields': ('is_active', 'code', 'email', 'first_name', 'last_name', 'password',)
        }),
    )
    readonly_fields = ('password',)
    list_display = ('id', 'email', 'first_name', 'last_name',)
    list_display_links = list_display
admin.site.register(User, UserAdmin)