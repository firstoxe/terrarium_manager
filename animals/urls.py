from django.urls import path, include

from . import views

app_name = 'animals'

urlpatterns = [
    path('', views.AnimalListView.as_view(), name='animal_list'),
    path('animal/<int:pk>/', views.AnimalDetailView.as_view(), name='animal_detail'),
    path('animal/create/', views.AnimalCreateView.as_view(), name='animal_create'),
    path('animal/<int:pk>/update/', views.AnimalUpdateView.as_view(), name='animal_update'),
    path('animal/<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal_delete'),
    path('animal/<int:animal_id>/action/create/', views.ActionCreateView.as_view(), name='action_create'),
    path('animal/<int:animal_id>/action/<int:pk>/delete/', views.ActionDeleteView.as_view(), name='action_delete'),
]

urlpatterns += [
    path('taxonomy/', views.TaxonomyListView.as_view(), name='taxonomy_list'),
    path('taxonomy/create/', views.TaxonomyCreateView.as_view(), name='taxonomy_create'),
    path('taxonomy/select/', views.TaxonomySelectView.as_view(), name='taxonomy_select'),
    path('taxonomy/<int:pk>/update/', views.TaxonomyUpdateView.as_view(), name='taxonomy_update'),
    path('taxonomy/<int:pk>/delete/', views.TaxonomyDeleteView.as_view(), name='taxonomy_delete'),

]
urlpatterns += [
    path('morph/create/', views.MorphCreateView.as_view(), name='morph_create'),
]
