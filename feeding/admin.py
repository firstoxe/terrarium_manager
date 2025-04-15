from django.contrib import admin
from .models import FoodItem, FeedingEvent, FeedingSchedule, FeedingRequirement


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_type', 'calcium_content', 'protein_content', 'vitamin_d3_content', 'requires_calcium', 'requires_vitamin_d3', 'requires_multivitamins')
    list_filter = ('food_type', 'requires_calcium', 'requires_vitamin_d3', 'requires_multivitamins')
    search_fields = ('name', 'description')


@admin.register(FeedingEvent)
class FeedingEventAdmin(admin.ModelAdmin):
    list_display = ('animal', 'food_item', 'quantity', 'cost', 'date', 'used_calcium', 'used_vitamin_d3', 'used_multivitamins')
    list_filter = ('animal', 'food_item', 'date', 'used_calcium', 'used_vitamin_d3', 'used_multivitamins')
    search_fields = ('animal__name', 'food_item__name')
    date_hierarchy = 'date'


@admin.register(FeedingSchedule)
class FeedingScheduleAdmin(admin.ModelAdmin):
    list_display = ('animal', 'food_item', 'frequency', 'quantity', 'start_date')
    list_filter = ('animal', 'food_item', 'frequency')
    search_fields = ('animal__name', 'food_item__name')
    date_hierarchy = 'start_date'


@admin.register(FeedingRequirement)
class FeedingRequirementAdmin(admin.ModelAdmin):
    list_display = ('taxonomy', 'age_group', 'food_type', 'insect_ratio', 'plant_ratio', 'frequency', 'quantity_per_feeding', 'calcium_frequency', 'vitamin_d3_frequency', 'multivitamin_frequency')
    list_filter = ('taxonomy', 'age_group', 'food_type', 'frequency', 'calcium_frequency', 'vitamin_d3_frequency', 'multivitamin_frequency')
    search_fields = ('taxonomy__species', 'taxonomy__scientific_name')
