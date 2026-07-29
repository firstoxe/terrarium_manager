from ..models import Animal


def animals_for_user(user):
    return Animal.objects.filter(owner=user).select_related('taxonomy', 'morph')


def animal_for_user(user, pk):
    return animals_for_user(user).get(pk=pk)
