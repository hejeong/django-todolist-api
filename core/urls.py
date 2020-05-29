from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from Todo.views import TodoViewSet
from . import views

# set up router and register the viewsets; does URL binding automatically
router = DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users', views.register_user),
    path('token', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify', views.check_user_token, name='token-verify'),
]
