from django.contrib import admin

from .models import User


# admin.site.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )


admin.site.register(User, UserAdmin)
