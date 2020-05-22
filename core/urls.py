from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from Todo.views import TodoViewSet


# set up router and register the viewsets; does URL binding automatically
router = DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
]
