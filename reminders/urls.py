from django.urls import path
from . import views

app_name = 'reminders'

urlpatterns = [
    path('', views.ReminderListView.as_view(), name='list'),
    path('generate/', views.ReminderGenerateView.as_view(), name='generate'),
    path('<int:pk>/done/', views.ReminderDoneView.as_view(), name='done'),
    path('<int:pk>/dismiss/', views.ReminderDismissView.as_view(), name='dismiss'),
]
