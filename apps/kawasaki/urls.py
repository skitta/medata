from django.urls import path, include
from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r'patients', views.PatientViewSet)
routers.register(r'bloodTests', views.BloodTestViewSet)
routers.register(r'liverFunction', views.LiverFunctionViewSet)
routers.register(r'echocardiography', views.EchocardiographyViewSet)
routers.register(r'enrollGroups', views.EnrollGroupViewSet)
routers.register('otherTests', views.OtherTestViewSet)
routers.register('samples', views.SamplesViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    # path('zscore/update/', views.update_z_score, name='update_z_score'),  # never use this!
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('summary/', views.PatientSummaryView.as_view(), name='summary'),
    path('count-by-month/', views.PatientCountByMonthView.as_view(), name='count'),
    path('age-by-group/', views.PatientAgeByGroupView.as_view(), name='age'),
]
