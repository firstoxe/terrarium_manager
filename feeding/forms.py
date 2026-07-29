from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML
from django import forms
from django.urls import reverse

from .models import FeedingSchedule


class FeedingScheduleForm(forms.ModelForm):
    class Meta:
        model = FeedingSchedule
        fields = ['interval_days', 'food_type', 'amount', 'is_active']
        widgets = {
            'interval_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'food_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, сверчки'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        cancel_url = reverse('feeding:schedule_list')
        self.helper.layout = Layout(
            Div(Field('food_type'), css_class='mb-3'),
            Div(
                Div(Field('interval_days'), css_class='col-md-6'),
                Div(Field('amount'), css_class='col-md-6'),
                css_class='row g-3 mb-3',
            ),
            Div(Field('is_active', wrapper_class='form-check'), css_class='mb-2'),
            HTML(
                f'<div class="tm-form-actions">'
                f'<button type="submit" class="btn btn-primary">Сохранить</button>'
                f'<a href="{cancel_url}" class="btn btn-outline-secondary">Отмена</a>'
                f'</div>'
            ),
        )
