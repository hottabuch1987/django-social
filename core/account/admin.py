from django.contrib import admin
from .models import Forum, User, UserImage, Notification


admin.site.register(User)

admin.site.register(Forum)



admin.site.register(Notification)

admin.site.register(UserImage)



