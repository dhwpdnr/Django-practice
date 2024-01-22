import pytest
from core_apps.users.forms import UserCreationForm
from core_apps.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_creation_form_vaild_data():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password1": "test_password1234",
        "password2": "test_password1234",
    }
    form = UserCreationForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_user_creation_form_invalid_data():
    user = UserFactory()
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": user.email,
        "password1": "test_password1234",
        "password2": "test_password1234",
    }
    form = UserCreationForm(data=data)
    assert not form.is_valid()
    assert "email" in form.errors
