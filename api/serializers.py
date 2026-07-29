from rest_framework import serializers, viewsets, permissions

from animals.models import Animal, Action
from feeding.models import FeedingLog


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, 'owner', None)
        if owner is not None:
            return owner == request.user
        animal = getattr(obj, 'animal', None)
        return animal is not None and animal.owner == request.user


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'name', 'taxonomy', 'morph', 'sex', 'birth_date', 'habitat', 'care_level', 'notes']

    def validate(self, attrs):
        taxonomy = attrs.get('taxonomy', getattr(self.instance, 'taxonomy', None))
        morph = attrs.get('morph', getattr(self.instance, 'morph', None))
        if morph and taxonomy and morph.taxonomy_id != taxonomy.id:
            raise serializers.ValidationError({'morph': 'Морф должен относиться к выбранной таксономии.'})
        return attrs


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'animal', 'action_type', 'date', 'description', 'cost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['animal'].queryset = Animal.objects.filter(owner=request.user)

    def validate_animal(self, animal):
        request = self.context.get('request')
        if request and animal.owner_id != request.user.id:
            raise serializers.ValidationError('Нельзя создавать действия для чужого животного.')
        return animal


class FeedingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingLog
        fields = ['id', 'animal', 'date', 'food_type', 'amount', 'notes']


class AnimalViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Action.objects.filter(animal__owner=self.request.user).select_related('animal')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FeedingLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedingLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return FeedingLog.objects.filter(animal__owner=self.request.user).select_related('animal')
