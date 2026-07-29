import csv
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView, View

from animals.models import Action
from animals.services.costs import total_costs_for_user


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        month_ago = timezone.now() - timedelta(days=30)

        context['monthly_costs'] = (
            Action.objects.filter(animal__owner=user, date__gte=month_ago)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('cost'))
            .order_by('month')
        )
        context['costs_by_taxonomy'] = (
            Action.objects.filter(animal__owner=user)
            .values('animal__taxonomy__species')
            .annotate(total=Sum('cost'))
            .order_by('-total')[:10]
        )
        context['total_costs'] = total_costs_for_user(user)
        return context


class ExportCSVView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="actions.csv"'
        writer = csv.writer(response)
        writer.writerow(['Дата', 'Животное', 'Тип', 'Описание', 'Затраты'])
        for action in Action.objects.filter(animal__owner=request.user).select_related('animal'):
            writer.writerow([
                action.date.strftime('%Y-%m-%d %H:%M'),
                action.animal.name,
                action.get_action_type_display(),
                action.description,
                action.cost,
            ])
        return response
