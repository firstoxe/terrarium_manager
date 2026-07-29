import pytest


@pytest.fixture(autouse=True)
def test_settings(settings):
    settings.STORAGES = {
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
    settings.ALLOWED_HOSTS = [*settings.ALLOWED_HOSTS, 'testserver']


@pytest.fixture
def user(db):
    from accounts.factories import UserFactory
    return UserFactory()


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client
