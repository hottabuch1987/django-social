from django.contrib import admin
from .models import Forum, User, UserImage, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'birth_date',  'gender', "tel",
                    'online_status', 'slug', 'date_joined')
    list_filter = ('birth_date', 'username', 'first_name', 'slug')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'slug') 
    ordering = ('date_joined',)


    def get_readonly_fields(self, request, obj=None):
        return ('slug','id',)



admin.site.register(Forum)

admin.site.register(Notification)

admin.site.register(UserImage)



