from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from animals.services.ownership import animals_for_user
from genetics.services.calculator import predict_offspring


class GeneticsCalculatorView(LoginRequiredMixin, TemplateView):
    template_name = 'genetics/calculator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals'] = animals_for_user(self.request.user).filter(sex__in=['M', 'F'])
        male_id = self.request.GET.get('male')
        female_id = self.request.GET.get('female')
        if male_id and female_id:
            animals = {str(a.pk): a for a in context['animals']}
            male = animals.get(male_id)
            female = animals.get(female_id)
            if male and female:
                genes_a = _genes_for_animal(male)
                genes_b = _genes_for_animal(female)
                context['predictions'] = predict_offspring(genes_a, genes_b)
                context['selected_male'] = male
                context['selected_female'] = female
        return context


def _genes_for_animal(animal):
    if not animal.morph:
        return []
    return [
        {
            'gene_name': mg.gene.name,
            'inheritance_type': mg.gene.inheritance_type,
            'genotype': mg.genotype,
        }
        for mg in animal.morph.genes.select_related('gene')
    ]
