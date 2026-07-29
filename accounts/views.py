from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.edit import UpdateView

from .middleware import ActivityLogMiddleware
from .models import User, ActivityLog
from .forms import CustomUserCreationForm, CustomUserChangeForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:registration_pending')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@staff_member_required
def user_approval_list(request):
    pending_users = User.objects.filter(is_approved=False, is_active=False)
    return render(request, 'accounts/user_approval_list.html',
                 {'pending_users': pending_users})


@staff_member_required
@require_POST
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id, is_approved=False)
    user.is_approved = True
    user.is_active = True
    user.save()
    return redirect('accounts:user_approval_list')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


@login_required
def track_activity(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            ActivityLog.objects.create(
                user=request.user,
                action='PROFILE_UPDATE',
                ip_address=ActivityLogMiddleware.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                additional_info={
                    'view': view_func.__name__,
                    'method': request.method
                }
            )
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def registration_pending(request):
    return render(request, 'accounts/registration_pending.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
