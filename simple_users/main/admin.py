from django.contrib import admin
from .models import AdvUser

# Register your models here.


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('is_active', 'ia_activated'),
              ('is_staff', 'is_superuser'), 'groups', 'user_permissions',
              ('last_login',))
    readonly_fields = ('last_login',)


admin.site.register(AdvUser, AdvUserAdmin)
