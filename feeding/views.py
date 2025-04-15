from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import FeedingEvent, FeedingRequirement
from .forms import FeedingEventForm
from animals.models import Animal


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from .models import FeedingEvent, FeedingSchedule, FoodItem, FeedingRequirement
from .forms import FeedingEventForm, FeedingScheduleForm, FoodItemForm, FeedingRequirementForm
from .tables import FeedingEventTable, FeedingScheduleTable, FoodItemTable, FeedingRequirementTable
from animals.models import Animal


class FeedingEventCreateView(LoginRequiredMixin, CreateView):
    model = FeedingEvent
    form_class = FeedingEventForm
    template_name = 'feeding/feeding_event_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        animal = Animal.objects.get(pk=self.kwargs['animal_id'], owner=self.request.user)
        kwargs['animal'] = animal
        return kwargs

    def form_valid(self, form):
        form.instance.animal = Animal.objects.get(pk=self.kwargs['animal_id'], owner=self.request.user)
        form.instance.created_by = self.request.user
        age_group = form.instance.animal.get_age_group()
        form.instance.requirement = form.instance.animal.taxonomy.feeding_requirements.filter(age_group=age_group).first()
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'event': {
                    'id': self.object.id,
                    'date': self.object.date.strftime('%d.%m.%Y %H:%M'),
                    'food_item': self.object.food_item.name,
                    'quantity': str(self.object.quantity),
                    'cost': str(self.object.cost) if self.object.cost else '-',
                }
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.kwargs['animal_id']})


class FeedingEventDeleteView(LoginRequiredMixin, DeleteView):
    model = FeedingEvent
    template_name = 'feeding/feeding_event_confirm_delete.html'

    def get_queryset(self):
        return FeedingEvent.objects.filter(animal__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.kwargs['animal_id']})

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Событие кормления успешно удалено.")
        return super().delete(request, *args, **kwargs)


class FeedingScheduleCreateView(LoginRequiredMixin, CreateView):
    model = FeedingSchedule
    form_class = FeedingScheduleForm
    template_name = 'feeding/feeding_schedule_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        animal = Animal.objects.get(pk=self.kwargs['animal_id'], owner=self.request.user)
        kwargs['animal'] = animal
        return kwargs

    def form_valid(self, form):
        form.instance.animal = Animal.objects.get(pk=self.kwargs['animal_id'], owner=self.request.user)
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'schedule': {
                    'id': self.object.id,
                    'food_item': self.object.food_item.name,
                    'frequency': self.object.get_frequency_display(),
                    'quantity': str(self.object.quantity),
                    'start_date': self.object.start_date.strftime('%d.%m.%Y'),
                    'notes': self.object.notes or '-',
                }
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.kwargs['animal_id']})


class FeedingScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = FeedingSchedule
    template_name = 'feeding/feeding_schedule_confirm_delete.html'

    def get_queryset(self):
        return FeedingSchedule.objects.filter(animal__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.kwargs['animal_id']})

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Расписание кормления успешно удалено.")
        return super().delete(request, *args, **kwargs)


class FoodItemListView(LoginRequiredMixin, SingleTableView):
    model = FoodItem
    table_class = FoodItemTable
    template_name = 'feeding/food_item_list.html'
    paginate_by = 10


class FoodItemCreateView(LoginRequiredMixin, CreateView):
    model = FoodItem
    form_class = FoodItemForm
    template_name = 'feeding/food_item_form.html'
    success_url = reverse_lazy('feeding:food_item_list')


class FoodItemUpdateView(LoginRequiredMixin, UpdateView):
    model = FoodItem
    form_class = FoodItemForm
    template_name = 'feeding/food_item_form.html'
    success_url = reverse_lazy('feeding:food_item_list')


class FoodItemDeleteView(LoginRequiredMixin, DeleteView):
    model = FoodItem
    template_name = 'feeding/food_item_confirm_delete.html'
    success_url = reverse_lazy('feeding:food_item_list')


class FeedingRequirementListView(LoginRequiredMixin, SingleTableView):
    model = FeedingRequirement
    table_class = FeedingRequirementTable
    template_name = 'feeding/feeding_requirement_list.html'
    paginate_by = 10


class FeedingRequirementCreateView(LoginRequiredMixin, CreateView):
    model = FeedingRequirement
    form_class = FeedingRequirementForm
    template_name = 'feeding/feeding_requirement_form.html'
    success_url = reverse_lazy('feeding:feeding_requirement_list')


class FeedingRequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = FeedingRequirement
    form_class = FeedingRequirementForm
    template_name = 'feeding/feeding_requirement_form.html'
    success_url = reverse_lazy('feeding:feeding_requirement_list')


class FeedingRequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = FeedingRequirement
    template_name = 'feeding/feeding_requirement_confirm_delete.html'
    success_url = reverse_lazy('feeding:feeding_requirement_list')
