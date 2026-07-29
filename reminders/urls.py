from django.urls import path
from . import views

app_name = 'reminders'

urlpatterns = [
    path('', views.ReminderListView.as_view(), name='list'),
    path('<int:pk>/done/', views.ReminderDoneView.as_view(), name='done'),
]
