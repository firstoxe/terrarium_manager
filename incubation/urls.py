from django.urls import path
from . import views

app_name = 'incubation'

urlpatterns = [
    path('', views.IncubationListView.as_view(), name='list'),
    path('<int:pk>/', views.IncubationDetailView.as_view(), name='detail'),
]
