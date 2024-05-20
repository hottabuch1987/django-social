from django.contrib import admin
from .models import Reviews, Forum, User, UserImage, Notification


admin.site.register(User)

admin.site.register(Forum)

admin.site.register(Reviews)

admin.site.register(Notification)

admin.site.register(UserImage)



