from django.urls import path
from . import views

app_name = 'feeding'

urlpatterns = [
    path('event/create/<int:animal_id>/', views.FeedingEventCreateView.as_view(), name='feeding_event_create'),
    path('event/<int:animal_id>/<int:pk>/delete/', views.FeedingEventDeleteView.as_view(), name='feeding_event_delete'),
    path('schedule/create/<int:animal_id>/', views.FeedingScheduleCreateView.as_view(), name='feeding_schedule_create'),
    path('schedule/<int:animal_id>/<int:pk>/delete/', views.FeedingScheduleDeleteView.as_view(), name='feeding_schedule_delete'),
    path('food/list/', views.FoodItemListView.as_view(), name='food_item_list'),
    path('food/create/', views.FoodItemCreateView.as_view(), name='food_item_create'),
    path('food/update/<int:pk>/', views.FoodItemUpdateView.as_view(), name='food_item_update'),
    path('food/delete/<int:pk>/', views.FoodItemDeleteView.as_view(), name='food_item_delete'),
    path('requirement/list/', views.FeedingRequirementListView.as_view(), name='feeding_requirement_list'),
    path('requirement/create/', views.FeedingRequirementCreateView.as_view(), name='feeding_requirement_create'),
    path('requirement/update/<int:pk>/', views.FeedingRequirementUpdateView.as_view(), name='feeding_requirement_update'),
    path('requirement/delete/<int:pk>/', views.FeedingRequirementDeleteView.as_view(), name='feeding_requirement_delete'),
]
