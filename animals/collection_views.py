from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Collection


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'animals/collection_list.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)
