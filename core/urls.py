from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Todo.views import TodoViewSet


# set up router and register the viewsets; does URL binding automatically
router = DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    path('', include(router.urls))
]