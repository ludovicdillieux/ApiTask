from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from todoapp.models import CategoryModel, EtatModel, MyUser, TaskModel

# from .serializers import TasksSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ["email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = MyUser(email=self.validated_data["email"])
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"current_password": "Does not match"})
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"


class EtatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatModel
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    etat = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = TaskModel
        fields = "__all__"

        extra_kwargs = {"etat": {"required": True}, "category": {"required": True}}


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["id", "value"]
