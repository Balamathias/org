from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, User

class UAdmin(UserAdmin):
    list_display = ('email', 'firstName', 'lastName', 'phone', 'is_staff', 'is_superuser', 'userId')
    search_field = ('email', 'firstName', 'lastName', 'phone')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)


admin.site.register(User, UAdmin)
admin.site.register(Organization)
admin.site.site_header = 'Organization Administration'