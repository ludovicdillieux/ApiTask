from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from todoapp.serializers import UserSerializer

from todoapp.serializers import PasswordChangeSerializer, RegistrationSerializer
from todoapp.utils import get_tokens_for_user

# Create your views here.


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        if "email" not in request.data or "password" not in request.data:
            return Response(
                {"msg": "Veuillez remplir tous les champs"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            request.user.is_active = True
            serializer = self.serializer_class(data=request.user, partial=True)
            if serializer.is_valid():
                account = serializer.save()
                account.is_active = True
                account.save()
            return Response(
                {"msg": "Login Success", **auth_data}, status=status.HTTP_200_OK
            )
        return Response(
            {"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        logout(request)
        serializer = self.serializer_class(data=request.user, partial=True)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = False
            account.save()
        return Response({"msg": "Vous êtes déconnecté."}, status=status.HTTP_200_OK)


class ModifyProfil(APIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        if "password" in request.data:
            return Response(
                {"msg": "Impossible de mettre à jour le password via cette URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            serializer.save()
        return Response(
            {"msg": "Modification de votre profil réussi"}, status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
