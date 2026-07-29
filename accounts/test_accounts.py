import pytest
from django.urls import reverse

from accounts.factories import UserFactory, PendingUserFactory, StaffUserFactory
from accounts.forms import CustomAuthenticationForm
from accounts.models import User


@pytest.mark.django_db
def test_register_creates_inactive_user(client):
    response = client.post(reverse('accounts:register'), {
        'username': 'newuser',
        'email': 'new@example.com',
        'phone': '+79991234567',
        'password1': 'ComplexPass123!',
        'password2': 'ComplexPass123!',
    })
    assert response.status_code == 302
    user = User.objects.get(username='newuser')
    assert user.is_active is False
    assert user.is_approved is False


@pytest.mark.django_db
def test_register_redirects_to_pending(client):
    response = client.post(reverse('accounts:register'), {
        'username': 'pending1',
        'email': 'p@example.com',
        'password1': 'ComplexPass123!',
        'password2': 'ComplexPass123!',
    })
    assert response.url == reverse('accounts:registration_pending')


@pytest.mark.django_db
def test_registration_pending_page(client):
    response = client.get(reverse('accounts:registration_pending'))
    assert response.status_code == 200
    assert 'одобрения' in response.content.decode().lower()


@pytest.mark.django_db
def test_unapproved_user_cannot_login():
    user = PendingUserFactory(is_active=True, is_approved=False)
    user.set_password('testpass123')
    user.save()
    form = CustomAuthenticationForm(data={'username': user.username, 'password': 'testpass123'})
    assert not form.is_valid()


@pytest.mark.django_db
def test_unapproved_superuser_can_login():
    user = UserFactory(is_superuser=True, is_staff=True, is_approved=False, is_active=True)
    user.set_password('testpass123')
    user.save()
    form = CustomAuthenticationForm(data={'username': user.username, 'password': 'testpass123'})
    assert form.is_valid()


@pytest.mark.django_db
def test_create_superuser_is_approved():
    user = User.objects.create_superuser('boss', 'boss@example.com', 'ComplexPass123!')
    assert user.is_approved is True
    assert user.is_active is True
    assert user.is_superuser is True


@pytest.mark.django_db
def test_approved_user_can_login(client):
    user = UserFactory()
    user.set_password('testpass123')
    user.save()
    response = client.post(reverse('accounts:login'), {
        'username': user.username,
        'password': 'testpass123',
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_approve_user_requires_post(client):
    staff = StaffUserFactory()
    pending = PendingUserFactory()
    client.force_login(staff)
    response = client.get(reverse('accounts:approve_user', args=[pending.id]))
    assert response.status_code == 405


@pytest.mark.django_db
def test_approve_user_activates_account(client):
    staff = StaffUserFactory()
    pending = PendingUserFactory()
    client.force_login(staff)
    response = client.post(reverse('accounts:approve_user', args=[pending.id]))
    assert response.status_code == 302
    pending.refresh_from_db()
    assert pending.is_active is True
    assert pending.is_approved is True


@pytest.mark.django_db
def test_approval_list_requires_staff(client):
    user = UserFactory()
    client.force_login(user)
    response = client.get(reverse('accounts:user_approval_list'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_approval_list_shows_pending(client):
    staff = StaffUserFactory()
    PendingUserFactory(username='waituser')
    client.force_login(staff)
    response = client.get(reverse('accounts:user_approval_list'))
    assert response.status_code == 200
    assert 'waituser' in response.content.decode()


@pytest.mark.django_db
def test_profile_requires_login(client):
    assert client.get(reverse('accounts:profile')).status_code == 302


@pytest.mark.django_db
def test_profile_for_authenticated_user(auth_client, user):
    response = auth_client.get(reverse('accounts:profile'))
    assert response.status_code == 200
    assert user.username in response.content.decode()


@pytest.mark.django_db
def test_profile_edit(auth_client, user):
    response = auth_client.get(reverse('accounts:profile_edit'))
    assert response.status_code == 200
    response = auth_client.post(reverse('accounts:profile_edit'), {
        'username': user.username,
        'email': 'updated@example.com',
        'phone': '+79990001122',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.email == 'updated@example.com'
