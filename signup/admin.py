from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email',
        'full_name',
        'phone_number',
        'university_of_study',
        'course',
        'year_of_admission',
        'year_of_graduation'
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'full_name', 
            'phone_number', 
            'university_of_study', 
            'course', 
            'year_of_admission', 
            'year_of_graduation'
        )}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'groups', 
            'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'password1', 
                'password2', 
                'full_name', 
                'phone_number', 
                'university_of_study', 
                'course', 
                'year_of_admission', 
                'year_of_graduation'
            ),
        }),
    )
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = [
        'user', 
        'university_of_study', 
        'course', 
        'year_of_admission', 
        'full_name', 
        'year_of_graduation'
    ]
    search_fields = ('user__email', 'university_of_study', 'course')
    ordering = ('user',)

admin.site.register(Profile, ProfileAdmin)