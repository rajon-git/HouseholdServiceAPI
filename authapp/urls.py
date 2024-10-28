from django.urls import path
from .views import RegisterView, LoginView, LogoutView, SendVerificationCodeView, ResetPasswordView, VerifyCodeView, ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-account/', VerifyCodeView.as_view(), name='verify-code'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', SendVerificationCodeView.as_view(), name='send-verification-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
]
