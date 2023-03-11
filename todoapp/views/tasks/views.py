# import datetime object
import math
from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from todoapp.models import EtatModel, TaskModel, MyUser, CategoryModel
from todoapp.serializers import EtatsSerializer, TasksSerializer, CategoriesSerializer

# create a class


class Etats(generics.GenericAPIView):
    serializer_class = EtatsSerializer
    queryset = EtatModel.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        etats = EtatModel.objects.all()
        total_etats = etats.count()
        serializer = self.serializer_class(etats, many=True)
        return Response(
            {
                "status": "success",
                "total": total_etats,
                "tasks": serializer.data,
            }
        )


class Category(generics.GenericAPIView):
    serializer_class = CategoriesSerializer
    queryset = CategoryModel.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        category = CategoryModel.objects.all()
        total_categories = category.count()
        serializer = self.serializer_class(category, many=True)
        return Response(
            {
                "status": "success",
                "total": total_categories,
                "tasks": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "note": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Tasks(generics.GenericAPIView):
    serializer_class = TasksSerializer
    queryset = TaskModel.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        tasks = self.queryset.filter(user=request.user)
        total_tasks = tasks.count()
        serializer = self.serializer_class(tasks, many=True)
        return Response(
            {
                "status": "success",
                "total": total_tasks,
                "tasks": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                etat=EtatModel.objects.get(value="à faire"),
                category=CategoryModel.objects.get(value="python"),
            )
            return Response(
                {"status": "success", "note": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TaskDetail(generics.GenericAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_task(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        task = self.get_task(pk=pk)
        if task == None:
            return Response(
                {"status": "fail", "message": f"task with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(task)
        return Response({"status": "success", "task": serializer.data})

    def patch(self, request, pk):
        task = self.get_task(pk)
        if task == None:
            return Response(
                {"status": "fail", "message": f"task with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(task, data=request.data, partial=True)
        if request.data.get("etat") is "" or request.data.get("category") is "":
            return Response(
                {
                    "status": "Fail",
                    "task": "L'état ou la catégorie ne peuvent pas être vide",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            serializer.validated_data["updatedAt"] = datetime.now()
            serializer.save()
            return Response({"status": "success", "task": serializer.data})
        return Response(
            {"status": "fail", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        task = self.get_task(pk)
        if task == None:
            return Response(
                {"status": "fail", "message": f"task with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskDetailByEtat(generics.GenericAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, etat):
        task = self.queryset.filter(etat=etat, user=request.user.id)
        if task == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"task with Id: {etat} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(task, many=True)
        return Response({"status": "success", "task": serializer.data})


class TaskDetailByCategory(generics.GenericAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, category):
        task = self.queryset.filter(category=category, user=request.user.id)
        if task == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"task with Id: {category} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(task, many=True)
        return Response({"status": "success", "task": serializer.data})


class TaskDetailByCategoryEtat(generics.GenericAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, category, etat):
        task = self.queryset.filter(category=category, etat=etat, user=request.user.id)
        if task == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"task with Id: {category} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(task, many=True)
        return Response({"status": "success", "task": serializer.data})
