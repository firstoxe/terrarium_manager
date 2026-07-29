from django.contrib import admin
from .models import FeedingSchedule, FeedingLog


@admin.register(FeedingSchedule)
class FeedingScheduleAdmin(admin.ModelAdmin):
    list_display = ('animal', 'interval_days', 'food_type', 'is_active', 'last_fed')
    list_filter = ('is_active',)
    search_fields = ('animal__name', 'food_type')


@admin.register(FeedingLog)
class FeedingLogAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'food_type', 'amount', 'created_by')
    list_filter = ('date',)
    search_fields = ('animal__name', 'food_type')
