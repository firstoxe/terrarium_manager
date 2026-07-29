from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from reminders.services import generate_reminders_for_user
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
        next_url = request.POST.get('next') or 'reminders:list'
        if next_url.startswith('/'):
            return redirect(next_url)
        return redirect('reminders:list')


class ReminderDismissView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
        reminder.status = 'DISMISSED'
        reminder.save(update_fields=['status'])
        return redirect('reminders:list')


class ReminderGenerateView(LoginRequiredMixin, View):
    def post(self, request):
        created = generate_reminders_for_user(request.user)
        messages.success(request, f'Обновлено напоминаний: {created}.')
        return redirect('reminders:list')
