from django.views.generic import TemplateView
from django.utils import timezone
from animals.models import Animal
from feeding.models import FeedingSchedule


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # if user.is_authenticated:
        #     context.update({
        #         'total_animals': Animal.objects.filter(owner=user).count(),
        #         'last_feeding': Feeding.objects.filter(animal__owner=user).last(),
        #         'upcoming_feeds': Feeding.objects.filter(
        #             animal__owner=user,
        #             date__gte=timezone.now()
        #         ).order_by('date')[:5],
        #
        #     })
        return context
