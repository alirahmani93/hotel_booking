from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.core.views import PlaceViewSet, RoomViewSet, ReserveViewSet, SearchAPIView

router = DefaultRouter()
router.register('place', PlaceViewSet, basename='place')
router.register('room', RoomViewSet, basename='room')
router.register('reserve', ReserveViewSet, basename='reserve')
urlpatterns = [
    path('api/search/', SearchAPIView.as_view()),

]
