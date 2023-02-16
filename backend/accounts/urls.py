from django.urls import path, include

from accounts.views import SignUpView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, profile, \
    LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', profile, name='accounts-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]
