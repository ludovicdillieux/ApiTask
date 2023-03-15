import pytest

from todoapp.models import CategoryModel, EtatModel, MyUser, TaskModel


@pytest.mark.django_db
def test_user_model_persists(create_test_user):
    assert MyUser.objects.count() > 0
    assert create_test_user.email == "test_user@test_user.com"
    assert create_test_user.password == "test_user"


@pytest.mark.django_db
def test_category_model_persists(create_test_category):
    assert CategoryModel.objects.count() > 0
    assert create_test_category.value == "autres"


@pytest.mark.django_db
def test_etat_model_persists(create_test_etat):
    assert EtatModel.objects.count() > 0
    assert create_test_etat.value == "en cours"


@pytest.mark.django_db
def test_task_model_persists(create_test_task):
    assert TaskModel.objects.count() > 0
    assert create_test_task.title == "new_post"
    assert create_test_task.content == "content"
    assert create_test_task.user.id == 1
    assert create_test_task.etat.id == 1
    assert create_test_task.category.id == 1
