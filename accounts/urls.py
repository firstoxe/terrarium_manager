from django.urls import path
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from . import views
from .forms import CustomAuthenticationForm
from .onboarding import OnboardingView

app_name = 'accounts'


@method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True), name='dispatch')
class RateLimitedLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('pending/', views.registration_pending, name='registration_pending'),
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
    path('telegram/link/', views.telegram_link, name='telegram_link'),
    path('telegram/webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('approval/list/', views.user_approval_list, name='user_approval_list'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('login/', RateLimitedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/emails/password_reset_email.html',
        subject_template_name='accounts/emails/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
