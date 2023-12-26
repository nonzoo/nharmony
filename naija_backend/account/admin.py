from django.contrib import admin

# Register your models here.
from .models import User, FriendRequest

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name','email']
    list_per_page = 50 

admin.site.register(FriendRequest)

