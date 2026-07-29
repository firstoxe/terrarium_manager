from django.urls import path

from . import views

app_name = 'health'

urlpatterns = [
    path('animal/<int:animal_id>/weight/', views.WeightLogCreateView.as_view(), name='weight_create'),
    path('animal/<int:animal_id>/record/', views.HealthRecordCreateView.as_view(), name='record_create'),
    path('animal/<int:animal_id>/shedding/', views.SheddingLogCreateView.as_view(), name='shedding_create'),
]
