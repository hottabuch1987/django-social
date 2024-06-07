from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API description",
        terms_of_service="https://www.youtube.com/channel/UCCLye31f_uhGnJk3Vl1dYtg",
        contact=openapi.Contact(email="varvar1987a@mail.ru"),
        license=openapi.License(name="my-api"),
    ),
    public=True,
)

urlpatterns = [
    # Products
    # User
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # Docs
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    # API
    path('user/<slug:slug>/', views.UserDetailViewSet.as_view({'get': 'list'}), name='user_detail'),
    path('forum/', views.ForumViewSet.as_view({'get': 'list'}), name='forum'),
    path('users/', views.AllUsersViewSet.as_view({'get': 'list'}), name='users'),


]





