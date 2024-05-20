from django.urls import path
from . import views
app_name = 'recommend'

urlpatterns = [
        
        path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
]