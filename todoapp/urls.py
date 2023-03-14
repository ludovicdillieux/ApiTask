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
    path("etats/", Etats.as_view()),
    path("categories/", Category.as_view()),
    path("tasks/", Tasks.as_view()),
    path("tasks/<str:pk>/", TaskDetail.as_view()),
    path("tasks/etat/<str:etat>/", TaskDetailByEtat.as_view()),
    path("tasks/category/<str:category>/", TaskDetailByCategory.as_view()),
    path(
        "tasks/category/etat/<str:category>/<str:etat>/",
        TaskDetailByCategoryEtat.as_view(),
    ),
    path("accounts/register", RegistrationView.as_view(), name="register"),
    path("accounts/login", LoginView.as_view(), name="login"),
    path("accounts/logout", LogoutView.as_view(), name="logout"),
    path("accounts/modify-profil", ModifyProfil.as_view(), name="modify"),
    path("accounts/change-password", ChangePasswordView.as_view(), name="change-password"),
    path(
        "accounts/token-refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
