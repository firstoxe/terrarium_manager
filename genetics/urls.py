from django.urls import path
from . import views

app_name = 'genetics'

urlpatterns = [
    path('calculator/', views.GeneticsCalculatorView.as_view(), name='calculator'),
]
