from django.urls import path
from .views import index, callback

app_name = 'anantalinebot'

urlpatterns = [
    path('', index, name='index'),
    path('callback/', callback, name='callback'),
]
