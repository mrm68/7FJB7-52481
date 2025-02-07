from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "name",
        "is_staff",
    ]
    # Define the fieldsets for displaying the user details
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("name",)}),
    )

    # Define the fieldsets for adding new users
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "name"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
