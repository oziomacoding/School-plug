# signup/urls.py

from django.urls import path
from .views import login_view, logout_view, request_password_reset, verify_reset_code, reset_password
from .views import primary_signup_view, educational_details_view, profile_picture_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/signup/', primary_signup_view, name='primary_signup'),
    path('api/signup/educational-details/', educational_details_view, name='educational_details'),
    path('api/signup/profile-picture/', profile_picture_view, name='profile_picture'),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/request_password_reset/', request_password_reset, name='request_password_reset'),
    path('api/verify_reset_code/', verify_reset_code, name='verify_reset_code'),
    path('api/reset_password/', reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)