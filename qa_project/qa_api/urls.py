from django.urls import path
from . import views

urlpatterns = [
    path('api/qa/', views.qa_view, name='qa_api'),
    path('debug/file/', views.debug_file_view, name='debug_file'),
]