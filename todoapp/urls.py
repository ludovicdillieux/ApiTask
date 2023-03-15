from django.urls import path
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
    TaskDetailByEtat,
    Tasks,
    TaskDetailByCategory,
    TaskDetailByCategoryEtat,
)

urlpatterns = [
    path("etats/", Etats.as_view(), name="get_etat"),
    path("categories/", Category.as_view(), name="get_category"),
    path("tasks/", Tasks.as_view(), name="get_tasks"),
    path("tasks/<str:pk>/", TaskDetail.as_view(), name="get_tasks_detail"),
    path(
        "tasks/etat/<str:etat>/", TaskDetailByEtat.as_view(), name="get_tasks_by_etat"
    ),
    path(
        "tasks/category/<str:category>/",
        TaskDetailByCategory.as_view(),
        name="get_tasks_by_cat",
    ),
    path(
        "tasks/category/etat/<str:category>/<str:etat>/",
        TaskDetailByCategoryEtat.as_view(),
        name="get_tasks_cat_etat",
    ),
    path("accounts/register", RegistrationView.as_view(), name="register"),
    path("accounts/login", LoginView.as_view(), name="login"),
    path("accounts/logout", LogoutView.as_view(), name="logout"),
    path("accounts/modify-profil", ModifyProfil.as_view(), name="modify"),
    path(
        "accounts/change-password", ChangePasswordView.as_view(), name="change-password"
    ),
    path(
        "accounts/token-refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
