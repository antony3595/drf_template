from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('grapelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),

    path('api/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
