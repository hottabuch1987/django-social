from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django_email_verification import urls as email_urls
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler404, handler403, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social')),#github
    path('social-auth/', include('social_django.urls', namespace='social-auth')), #vk
    path('users/', include('shop.urls', namespace='shop')),
    path('account/', include('account.urls', namespace='account')),
    path('email/', include(email_urls), name='email-verification'),
    path("recommend/", include('recommend.urls', namespace='recommend')),
    path('rooms/', include('room.urls'), name='rooms'),
    path('direct_messages/', include('direct_messages.urls'), name='direct_messages'),
    path('', views.index, name='index'), 
]

urlpatterns += [
    #path("i18n/", include("django.conf.urls.i18n")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

handler404 = 'shop.views.error_404'
handler403 = 'shop.views.error_403'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
