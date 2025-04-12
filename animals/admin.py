from django.contrib import admin
from .models import Animal, Species

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')
    search_fields = ('name', 'scientific_name')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'owner', 'birth_date')
    list_filter = ('species', 'sex')
    search_fields = ('name', 'notes')
