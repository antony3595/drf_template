from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from main import settings

schema_view = get_schema_view(
    openapi.Info(
        title=settings.SITE_NAME,
        default_version='v1',
        description="Django API template",
        terms_of_service="",
        contact=openapi.Contact(email="antony3595@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('grapelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),

    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
