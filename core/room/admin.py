from django.contrib import admin
from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon_html']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = [ 'name','slug']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'content', 'date_added']
    list_filter = [ 'user','room']