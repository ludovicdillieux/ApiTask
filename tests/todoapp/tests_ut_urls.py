from django.urls import resolve, reverse
from rest_framework_simplejwt import views as jwt_views

from todoapp.views.authentification.views import (
    ChangePasswordView,
    LoginView,
    LogoutView,
    ModifyProfil,
    RegistrationView,
)
from todoapp.views.tasks.views import (
    Category,
    Etats,
    TaskDetail,
    TaskDetailByCategory,
    TaskDetailByCategoryEtat,
    TaskDetailByEtat,
    Tasks,
)


def test_etat():
    response = reverse("get_etat")
    resolver = resolve(response)
    assert resolver.func.cls == Etats


def test_category():
    response = reverse("get_category")
    resolver = resolve(response)
    assert resolver.func.cls == Category


def test_task():
    response = reverse("get_tasks")
    resolver = resolve(response)
    assert resolver.func.cls == Tasks


def test_task_detail():
    response = reverse("get_tasks_detail", args="1")
    resolver = resolve(response)
    assert resolver.func.cls == TaskDetail


def test_task_by_etat():
    response = reverse("get_tasks_by_etat", args="1")
    resolver = resolve(response)
    assert resolver.func.cls == TaskDetailByEtat


def test_task_by_cat():
    response = reverse("get_tasks_by_cat", args="1")
    resolver = resolve(response)
    assert resolver.func.cls == TaskDetailByCategory


def test_task_by_cat_etat():
    response = reverse("get_tasks_cat_etat", args=("1", "2"))
    resolver = resolve(response)
    assert resolver.func.cls == TaskDetailByCategoryEtat


def test_register():
    response = reverse("register")
    resolver = resolve(response)
    assert resolver.func.cls == RegistrationView


def test_login():
    response = reverse("login")
    resolver = resolve(response)
    assert resolver.func.cls == LoginView


def test_logout():
    response = reverse("logout")
    resolver = resolve(response)
    assert resolver.func.cls == LogoutView


def test_modify():
    response = reverse("modify")
    resolver = resolve(response)
    assert resolver.func.cls == ModifyProfil


def test_change_password():
    response = reverse("change-password")
    resolver = resolve(response)
    assert resolver.func.cls == ChangePasswordView


def test_token_refresh():
    response = reverse("token_refresh")
    resolver = resolve(response)
    assert resolver.func.cls == jwt_views.TokenRefreshView
