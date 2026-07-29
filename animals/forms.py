from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, Row, Field, HTML
from django import forms
from django.urls import reverse
from django_select2.forms import ModelSelect2Widget

from .models import Animal, Action, Taxonomy, Morph


class MySelect2WidgetMorph(ModelSelect2Widget):
    max_results = 25
    search_fields = ['name__icontains']
    dependent_fields = {'taxonomy': 'taxonomy'}

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({
            'data-dropdown-parent': '#morph-container',
            'data-placeholder': 'Выберите морфу (если есть)',
            'data-allow-clear': 'true',
            'style': 'width: 100%;'
        })
        return attrs



class MySelect2WidgetTaxonomy(ModelSelect2Widget):
    max_results = 25
    model = Taxonomy
    search_fields = ['species__icontains', 'scientific_name__icontains']

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({
            'id': 'id_taxonomy_animal',
            'data-dropdown-parent': '#taxonomy-container',
            'data-placeholder': 'Выберите таксон',
            'data-allow-clear': 'true',
            'style': 'width: 100%;'
        })
        return attrs



class MySelect2WidgetMorphTaxonomy(ModelSelect2Widget):  # Новый виджет для MorphForm
    max_results = 25
    model = Taxonomy
    search_fields = ['species__icontains', 'scientific_name__icontains']

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({
            'id': 'id_taxonomy_morph',
            'data-dropdown-parent': '#morph-container2',
            'data-placeholder': 'Выберите таксон',
            'data-allow-clear': 'true',
            'style': 'width: 100%;'
        })
        return attrs


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'taxonomy', 'morph', 'birth_date', 'acquisition_date', 'sex', 'photo', 'notes', 'habitat', 'care_level']
        widgets = {
            'taxonomy': MySelect2WidgetTaxonomy(attrs={'data-minimum-input-length': 0, 'style': 'width: 100%;'}),
            'morph': MySelect2WidgetMorph(attrs={'data-minimum-input-length': 0, 'style': 'width: 100%;'}),
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Выберите дату'
                },
                format='%Y-%m-%d'),
            'acquisition_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Выберите дату'
                },
                format='%Y-%m-%d'),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'habitat': forms.Select(attrs={'class': 'form-control'}),
            'care_level': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        self.fields['taxonomy'].queryset = Taxonomy.objects.all().order_by('scientific_name')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-small'
        self.helper.label_class = ''
        library_url = reverse('animals:species_library')
        photo_field = Div(
            HTML('''
                        {% if form.instance.photo %}
                            <img src="{{ form.instance.photo.url }}" class="img-fluid rounded mb-2" style="max-width: 200px;">
                            <p><a href="#" onclick="document.getElementById('id_photo').value='';this.remove();return false;">Удалить фото</a></p>
                        {% endif %}
                    '''),
            Field('photo', css_class='form-control'),
            css_class='col-md-6 mb-3'
        )

        self.helper.layout = Layout(
            HTML(
                f'<div class="alert alert-info mb-3">'
                f'<strong>Рекомендуем:</strong> сначала выберите вид в '
                f'<a href="{library_url}">справочнике</a> и нажмите «Добавить в базу» — '
                f'тогда уход и морфы подтянутся автоматически.'
                f'</div>'
            ),
            Row(
                Div(Field('name', css_class='form-control'), css_class='col-md-6 mb-3'),
                Div(
                    Field('taxonomy', css_class='form-control '),
                    HTML(
                        f'<a href="{library_url}" class="btn btn-primary btn-sm mt-2 me-2">Выбрать из справочника</a>'
                        '<button type="button" class="btn btn-outline-secondary btn-sm mt-2" id="add-taxonomy-btn" '
                        'data-bs-toggle="modal" data-bs-target="#taxonomyModal">Редкий вид вручную</button>'
                    ),
                    css_class='col-md-6 mb-3', id='taxonomy-container'
                ),
            ),
            Row(
                Div(
                    Field('morph', css_class='form-control'),
                    HTML(
                        '<button type="button" class="btn btn-outline-secondary btn-sm mt-2" id="add-morph-btn" '
                        'data-bs-toggle="modal" data-bs-target="#morphModal">Добавить морфу</button>'
                    ),
                    css_class='col-md-6 mb-3', id='morph-container'
                ),
                Div(Field('sex', css_class='form-control'), css_class='col-md-6 mb-3'),
            ),
            Row(
                Div(Field('birth_date', css_class='form-control'), css_class='col-md-6 mb-3'),
                Div(Field('acquisition_date', css_class='form-control'), css_class='col-md-6 mb-3'),
            ),
            Row(
                Div(Field('habitat', css_class='form-control'), css_class='col-md-6 mb-3'),
                Div(Field('care_level', css_class='form-control'), css_class='col-md-6 mb-3'),
            ),
            Row(
                photo_field,
            ),
            Row(
                Div(Field('notes', css_class='form-control'), css_class='col-12 mb-3'),
            ),
            FormActions(
                HTML(
                    f'<div class="tm-form-actions">'
                    f'<button type="submit" class="btn btn-primary">Сохранить</button>'
                    f'<a href="{reverse("animals:animal_list")}" class="btn btn-outline-secondary">Отмена</a>'
                    f'</div>'
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        taxonomy = cleaned_data.get('taxonomy')
        morph = cleaned_data.get('morph')
        if morph and morph.taxonomy != taxonomy:
            raise forms.ValidationError("Морфа должна соответствовать выбранному таксону.")
        return cleaned_data


class TaxonomyForm(forms.ModelForm):
    class Meta:
        model = Taxonomy
        fields = ['class_name', 'order', 'family', 'genus', 'species', 'subspecies', 'scientific_name']
        widgets = {
            'class_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Reptilia'}),
            'order': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Squamata'}),
            'family': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Gekkonidae'}),
            'genus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Eublepharis'}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, macularius'}),
            'subspecies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, afghanicus'}),
            'scientific_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Например, Eublepharis macularius'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('class_name', css_class='form-control'),
            Field('order', css_class='form-control'),
            Field('family', css_class='form-control'),
            Field('genus', css_class='form-control'),
            Field('species', css_class='form-control'),
            Field('subspecies', css_class='form-control'),
            Field('scientific_name', css_class='form-control'),
        )


class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['action_type', 'description', 'cost']
        widgets = {
            'action_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-small'
        self.helper.layout = Layout(
            Field('action_type', css_class='form-select mb-3'),
            Field('description', css_class='form-control mb-3'),
            Field('cost', css_class='form-control mb-3'),
            FormActions(
                HTML(
                    '<div class="tm-form-actions">'
                    '<button type="submit" class="btn btn-primary">Добавить действие</button>'
                    '<button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Отмена</button>'
                    '</div>'
                ),
            ),
        )

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if cost is not None and cost < 0:
            raise forms.ValidationError("Затраты не могут быть отрицательными.")
        return cost

class MorphForm(forms.ModelForm):


    class Meta:
        model = Morph
        fields = ['taxonomy', 'name', 'description']
        widgets = {
            'taxonomy': MySelect2WidgetMorphTaxonomy(attrs={'data-minimum-input-length': 0}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Albino'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Описание морфы'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('taxonomy', css_class='form-control'),
                css_class='mb-3', id='morph-taxonomy-container'
            ),
            Field('name', css_class='form-control'),
            Field('description', css_class='form-control'),
        )


