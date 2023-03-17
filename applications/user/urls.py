from rest_framework.routers import DefaultRouter

from applications.user.views import UserViewSet, OwnerViewSet, AuthViewSet

router = DefaultRouter()
router.register('auth', AuthViewSet, 'auth')
router.register('user', UserViewSet, 'user')
router.register('owner', OwnerViewSet, 'owner')
