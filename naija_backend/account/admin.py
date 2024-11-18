from django.contrib import admin

# Register your models here.
from .models import User, FriendRequest, Categories

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('name', 'email','gender','age','categories','locations')
    search_fields = ['name','email']
    list_per_page = 50 

admin.site.register(FriendRequest)
admin.site.register(Categories)

