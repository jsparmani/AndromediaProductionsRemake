from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    path('import-all/<str:channel_id>/', views.import_all, name='import_all')
]
