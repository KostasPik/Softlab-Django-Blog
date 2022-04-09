from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_premium', 'email_verified']
    fieldsets = (
    *UserAdmin.fieldsets,  # original form fieldsets, expanded
    (                      # new fieldset added on to the bottom
        'CustomUser Fields',  # group heading of your choice; set to None for a blank space instead of a header
        {
            'fields': (
                'email_verified','is_premium',
            ),
        },
    ),
)


admin.site.register(CustomUser, CustomUserAdmin)
