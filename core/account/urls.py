from  django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from  . import views
from django.shortcuts import render
from .views import ForumView

app_name = 'account'

urlpatterns = [
    #register and verification
    path('register/', views.register_user, name='register'),
    path('email-verification-sent/', lambda request:render(request, 'account/email/email_vertification_sent.html'), name='email-verification-sent'),
    
    #login and logout
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    #dashboard
    path('dashboard/', views.DashboardUserView.as_view(), name='dashboard'),
    path('profile-management/', views.profile_user, name='profile-management'),
    path('delete-user/', views.delete_user, name='delete-user'),
    path('users/<slug:slug>/', views.user_detail, name='user_detail'),

    #password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password-reset.html',
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')),
        name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password-reset-done.html'),
        name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password-reset-confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')),
        name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password-reset-complete.html'),
        name='password_reset_complete'),

    #reviews
    path('reviews/', views.reviews, name='reviews'),

    #forum 
    path('message/send/', ForumView.as_view(), name="send_message"),

   

]