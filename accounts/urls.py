from django.urls import path

from .views import  activate, password_reset_request, signup
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('signup/', signup, name='signup'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    # path('password_reset/', name="password_reset"),
    # path('password_reset/done/', name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', name="password_reset_confirm"),
    # path('reset/done/', name="password_reset_confirm"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      
   
]