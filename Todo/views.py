from rest_framework import viewsets

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    This provides 'list', 'create', 'retrieve', 'update' and 'destroy actions for Todo
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer