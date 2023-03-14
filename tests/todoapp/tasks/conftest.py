import pytest
from django.test import TestCase
from todoapp.models import CategoryModel, EtatModel, MyUser, TaskModel


# @pytest.mark.django_db
# def test_register_success(self):
#     superuser = MyUser.objects.create_superuser(
#         email="admin@admin.com", password="admin"
#     )
#     superuser.save()
#     assert MyUser.objects.count() > 0


@pytest.mark.django_db
@pytest.fixture
def create_test_user():
    test_user = MyUser.objects.create(
        id=1, email="test_user@test_user.com", password="test_user"
    )
    test_user.save()
    return test_user


@pytest.mark.django_db
@pytest.fixture
def create_test_category():
    cat = CategoryModel.objects.create(id=1, value="autres")
    cat.save()

    return cat


@pytest.mark.django_db
@pytest.fixture
def create_test_etat():
    etat = EtatModel.objects.create(id=1, value="en cours")
    etat.save()

    return etat


@pytest.mark.django_db
@pytest.fixture
def create_test_task(create_test_etat, create_test_category, create_test_user):
    task = TaskModel.objects.create(
        title="new_post",
        content="content",
        user=MyUser(id=create_test_user.id),
        etat=EtatModel(id=create_test_etat.id),
        category=CategoryModel(id=create_test_category.id),
    )
    task.save()

    return task
