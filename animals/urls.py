from django.urls import path, include

from . import views, collection_views, library_views

app_name = 'animals'

urlpatterns = [
    path('', views.AnimalListView.as_view(), name='animal_list'),
    path('collections/', collection_views.CollectionListView.as_view(), name='collection_list'),
    path('create/', views.AnimalCreateView.as_view(), name='animal_create'),
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='animal_detail'),
    path('<int:pk>/update/', views.AnimalUpdateView.as_view(), name='animal_update'),
    path('<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal_delete'),
    path('<int:animal_id>/action/add/', views.ActionCreateView.as_view(), name='action_create'),
]

urlpatterns += [
    path('taxonomy/create/', views.TaxonomyCreateView.as_view(), name='taxonomy_create'),
    path('taxonomy/select/', views.TaxonomySelectView.as_view(), name='taxonomy_select'),
    path('morph/create/', views.MorphCreateView.as_view(), name='morph_create'),
    path('library/', library_views.SpeciesLibraryListView.as_view(), name='species_library'),
    path('library/<slug:library_id>/import/', library_views.SpeciesLibraryImportView.as_view(), name='species_library_import'),
]
