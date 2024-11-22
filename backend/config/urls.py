from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import AIAgentViewSet

router = DefaultRouter()
router.register(r'ai', AIAgentViewSet, basename='ai')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] 