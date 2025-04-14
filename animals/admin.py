# animals/admin.py
from django.contrib import admin
from .models import Animal, Taxonomy, Morph, Action, CareRequirement


@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('species', 'scientific_name', 'genus', 'family')
    search_fields = ('species', 'scientific_name', 'genus', 'family', 'class_name', 'order')
    list_filter = ('class_name', 'order', 'family')
    ordering = ('species',)


@admin.register(Morph)
class MorphAdmin(admin.ModelAdmin):
    list_display = ('name', 'taxonomy', 'description')
    search_fields = ('name', 'description', 'taxonomy__species')
    list_filter = ('taxonomy',)
    ordering = ('name',)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'taxonomy', 'morph', 'owner', 'birth_date', 'habitat', 'care_level')
    list_filter = ('taxonomy', 'morph', 'sex', 'habitat', 'care_level', 'owner')
    search_fields = ('name', 'notes', 'taxonomy__species', 'taxonomy__scientific_name')
    ordering = ('-acquisition_date',)
    raw_id_fields = ('taxonomy', 'morph', 'owner')  # Для удобства выбора при большом количестве записей
    list_select_related = ('taxonomy', 'morph', 'owner')  # Оптимизация запросов


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('animal', 'action_type', 'date', 'created_by')
    search_fields = ('description', 'animal__name', 'animal__taxonomy__species')
    list_filter = ('action_type', 'date', 'created_by')
    ordering = ('-date',)
    raw_id_fields = ('animal', 'created_by')
    list_select_related = ('animal', 'created_by')


@admin.register(CareRequirement)
class CareRequirementAdmin(admin.ModelAdmin):
    list_display = ('taxonomy', 'temperature_min', 'temperature_max', 'humidity_min', 'humidity_max')
    search_fields = ('taxonomy__species', 'taxonomy__scientific_name', 'diet')
    list_filter = ('taxonomy',)
    ordering = ('taxonomy__species',)
    raw_id_fields = ('taxonomy',)
    list_select_related = ('taxonomy',)
