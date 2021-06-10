"""crud_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from api.views import *
from api import views
from rest_framework.routers import DefaultRouter  # for ViewSet class

router = DefaultRouter()

router.register('student.api', views.StudentViewSet, basename='Student')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student.api/', StudentAPI.as_view()),
    path('', include(router.urls)),
]
