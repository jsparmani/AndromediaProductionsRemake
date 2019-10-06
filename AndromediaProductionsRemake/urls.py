"""AndromediaProductionsRemake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views

admin.site.site_header = "Andromedia Productions"
admin.site.site_title = "Andromedia Productions Portal"
admin.site.index_title = "Welcome to Andromedia Productions"

urlpatterns = [
    path('control-panel/', admin.site.urls),
    path('user/', include('user.urls')),
    path('video/', include('video.urls')),
    path('', views.home, name='home'),
    path('play-video/<str:video_id>/', views.video_play, name='video_play')
]
