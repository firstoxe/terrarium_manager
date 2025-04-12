from django.urls import path, include

from . import views

app_name = 'animals'

urlpatterns = [
    path('', views.AnimalListView.as_view(), name='list'),
path("select2/", include("django_select2.urls")),
    path('create/', views.AnimalCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.AnimalUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='delete'),
]

urlpatterns += [
    path('species/create/', views.SpeciesCreateView.as_view(), name='species_create'),
    path('species/select/', views.SpeciesSelectView.as_view(), name='species_select'),
]
