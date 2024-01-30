from django.urls import path

from . import api

urlpatterns = [
    path('', api.notifications, name = 'notifications'),
    path('read/<uuid:pk>/',api.notification_read, name='notification read')
]