from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from applications.user.urls import router as user_router
from applications.core.urls import router as core_router, urlpatterns as url_
from applications.common.urls import router as common_router

router = DefaultRouter(trailing_slash=True)
router.registry.extend(common_router.registry)
router.registry.extend(user_router.registry)
router.registry.extend(core_router.registry)

admin.AdminSite.site_header = settings.SITE_HEADER
admin.AdminSite.site_title = settings.SITE_TITLE

urlpatterns = [
    path('', lambda x: redirect('admin/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view()),

]
urlpatterns += url_

urlpatterns += i18n_patterns(
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
