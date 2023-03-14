from django.contrib import admin
from todoapp.models import EtatModel, MyUser, TaskModel, CategoryModel
# Register your models here.
admin.site.register(EtatModel)
admin.site.register(TaskModel)
admin.site.register(CategoryModel)
admin.site.register(MyUser)