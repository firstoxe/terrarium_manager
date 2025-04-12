from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, Row, Field, HTML
from django import forms
from django_select2.forms import ModelSelect2Widget

from .models import Animal, Species


class MySelect2WidgetSpecies(ModelSelect2Widget):
    max_results = 25
    search_fields = [
        'name__icontains',
    ]

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-dropdown-parent'] = '#species-container'
        return attrs


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'species', 'birth_date', 'sex', 'photo', 'notes']
        widgets = {
            'species': MySelect2WidgetSpecies(attrs={'data-minimum-input-length': 0, 'style': 'width: 100%;'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = ''

        submit_btn = HTML(
            '<button type="submit" class="btn btn-primary" id="submit-id-animal_submit">'
            '<i class="bi bi-save"></i> Сохранить животное'
            '</button>'
        )

        cancel_btn = HTML(
            '<button type="button" class="btn btn-secondary ms-2" data-bs-dismiss="modal">'
            '<i class="bi bi-x-circle"></i> Отмена'
            '</button>'
        )

        self.helper.form_class = 'small'

        self.helper.layout = Layout(
            Row(
                Div(
                    Field('name', css_class='form-control form-control-sm'),
                    css_class='form-group col-md-8 mb-0'
                ),
            ),
            Row(
                Div(
                    Field('species', css_class='form-control form-control-sm position-relative'),
                    css_class='form-group col-md-8 mb-0 position-relative',
                    id="species-container"
                ),
            ),
            Row(
                Div(
                    Field('birth_date', css_class='form-control form-control-sm'),
                    css_class='form-group col-md-6 mb-0'
                ),
                Div(
                    Field('sex', css_class='form-control form-control-sm'),
                    css_class='form-group col-md-6 mb-0'
                ),
            ),
            Row(
                Div(
                    Field('photo', css_class='form-control form-control-sm'),
                    css_class='form-group col-md-4 mb-0'
                ),
            ),
            Row(
                Div(
                    Field('notes', css_class='form-control form-control-sm', rows=3),
                    css_class='form-group col-md-8 mb-0'
                ),
            ),
            FormActions(
                submit_btn,
                cancel_btn
            )
        )


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = Species
        fields = ['name', 'scientific_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'scientific_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
