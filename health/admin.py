from django.contrib import admin
from .models import WeightLog, HealthRecord, SheddingLog


@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'weight_g')


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'reason', 'next_visit_date', 'cost')
    list_filter = ('date',)


@admin.register(SheddingLog)
class SheddingLogAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'quality')
