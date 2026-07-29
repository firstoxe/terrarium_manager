from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        required=False,
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+79991234567',
            'autocomplete': 'tel',
        }),
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
            'autocomplete': 'email',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'new-password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79991234567'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'username',
            'placeholder': 'Имя пользователя',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'current-password',
            'placeholder': 'Пароль',
        })

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        # Staff/superuser must always be able to log in — otherwise nobody
        # can approve pending registrations (createsuperuser bootstrap case).
        if user.is_staff or user.is_superuser:
            return
        if not user.is_approved:
            raise ValidationError(
                _('Ваша учётная запись ещё не одобрена администратором.'),
                code='not_approved',
            )
