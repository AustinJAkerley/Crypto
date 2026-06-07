from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.current_user, name='current_user'),
    
    # Crypto endpoints
    path('crypto/rsa/keygen/', views.rsa_keygen, name='rsa_keygen'),
    path('crypto/rsa/encrypt/', views.rsa_encrypt, name='rsa_encrypt'),
    path('crypto/rsa/decrypt/', views.rsa_decrypt, name='rsa_decrypt'),
    path('crypto/dh/exchange/', views.dh_exchange, name='dh_exchange'),
]
