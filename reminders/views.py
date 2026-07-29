from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from django.urls import reverse_lazy

from .models import Reminder


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'reminders/reminder_list.html'
    context_object_name = 'reminders'

    def get_queryset(self):
        return Reminder.objects.filter(
            user=self.request.user, status='PENDING',
        ).select_related('animal').order_by('due_date')


class ReminderDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
        reminder.status = 'DONE'
        reminder.save(update_fields=['status'])
        return redirect('reminders:list')
