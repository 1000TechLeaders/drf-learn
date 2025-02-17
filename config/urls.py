"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from csp.decorators import csp_exempt
from django.conf.urls import handler404
from django.conf.urls import handler500
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

handler404 = 'tasks.views.custom_404_view' # noqa
handler500 = 'tasks.views.custom_500_view' # noqa


urlpatterns = [
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('docs/',
         staff_member_required(
         csp_exempt(SpectacularSwaggerView.as_view(url_name='schema')),
         login_url='/oidc/authenticate'),
         name='swagger-ui'),
    path('redoc/',
         csp_exempt(SpectacularRedocView.as_view(url_name='schema')),
         name='redoc'),
    # tokens
    path('api/token/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    path(r'ht/', include('health_check.urls')),
    path('', include('django_prometheus.urls')),
]
