from rest_framework.routers import DefaultRouter
from applications.common.views import AppViewSet

router = DefaultRouter()

router.register('app', AppViewSet, basename='app')
