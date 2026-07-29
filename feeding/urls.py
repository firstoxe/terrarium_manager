from django.urls import path
from . import views

app_name = 'feeding'

urlpatterns = [
    path('', views.FeedingScheduleListView.as_view(), name='schedule_list'),
    path('history/', views.FeedingHistoryView.as_view(), name='history'),
    path('animal/<int:animal_id>/schedule/add/', views.FeedingScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/<int:pk>/edit/', views.FeedingScheduleUpdateView.as_view(), name='schedule_edit'),
    path('animal/<int:animal_id>/feed/', views.FeedTodayView.as_view(), name='feed_today'),
]
