"""visitor_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

# JWT codes
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('accounts/', include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),

    # path('api-auth/', include('rest_framework.urls')),
    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # custom authentication
    path('authentication/', include("authentication.urls")),
    # app urls
    path('', include("dashboard.urls")),
    path('visitor/', include("visitormanagement.urls")),
    path('department/', include("department.urls")),
    path('employee/', include("employee.urls")),
    path('purpose/', include("visitingpurpose.urls")),
    path('analytics/', include("analytics.urls")),
    path('visitor_token/', include("visitor_token.urls")),
    path('hijack/', include('hijack.urls')),
    path('otp-system/', include('otp_system.urls')),
    # path('visitor_app_admin/',include("visitor_app_admin.urls")),

]
