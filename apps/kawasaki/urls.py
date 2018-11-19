from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='kawasaki'),
    path('zscore/update/', views.update_z_score, name='update_z_score'),
]