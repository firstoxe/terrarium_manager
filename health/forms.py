from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

from .models import WeightLog, HealthRecord, SheddingLog


class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight_g', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight_g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('date'), Field('weight_g'), Field('notes'),
            HTML('<div class="tm-form-actions"><button type="submit" class="btn btn-primary">Сохранить вес</button></div>'),
        )


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = [
            'date', 'reason', 'diagnosis', 'treatment',
            'vet_name', 'cost', 'next_visit_date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'vet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'next_visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('date'), Field('reason'), Field('diagnosis'), Field('treatment'),
            Field('vet_name'), Field('cost'), Field('next_visit_date'),
            HTML('<div class="tm-form-actions"><button type="submit" class="btn btn-primary">Сохранить запись</button></div>'),
        )


class SheddingLogForm(forms.ModelForm):
    class Meta:
        model = SheddingLog
        fields = ['date', 'quality', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quality': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('date'), Field('quality'), Field('notes'),
            HTML('<div class="tm-form-actions"><button type="submit" class="btn btn-primary">Сохранить линьку</button></div>'),
        )
