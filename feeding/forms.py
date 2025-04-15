from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Row, Div, Field, HTML
from .models import FeedingEvent, FeedingRequirement, FoodItem, FeedingSchedule


class FeedingEventForm(forms.ModelForm):
    class Meta:
        model = FeedingEvent
        fields = ['food_item', 'quantity', 'cost', 'used_calcium', 'used_vitamin_d3', 'used_multivitamins']
        widgets = {
            'food_item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'used_calcium': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'used_vitamin_d3': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'used_multivitamins': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, animal=None, **kwargs):
        super().__init__(*args, **kwargs)
        if animal:
            self.fields['food_item'].queryset = animal.taxonomy.allowed_foods.all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-small'
        self.helper.label_class = ''
        self.helper.layout = Layout(
            Row(Div(Field('food_item', css_class='form-control'),)),
            Row(Div(Field('quantity', css_class='form-control'),)),
            Row(Div(Field('cost', css_class='form-control'),)),
            Row(
                Div(Field('used_calcium', css_class='form-check-input'), css_class='form-check'),
                Div(Field('used_vitamin_d3', css_class='form-check-input'), css_class='form-check ms-3'),
                Div(Field('used_multivitamins', css_class='form-check-input'), css_class='form-check ms-3'),
            ),
            FormActions(
                HTML('<button type="submit" class="btn btn-primary mt-2"><i class="bi bi-save"></i> Добавить кормление</button>'),
                HTML('<button type="button" class="btn btn-secondary mt-2 ms-2" data-bs-dismiss="modal"><i class="bi bi-x-circle"></i> Отмена</button>'),
            ),
        )

    def clean_food_item(self):
        food_item = self.cleaned_data.get('food_item')
        animal = self.instance.animal
        if food_item not in animal.taxonomy.allowed_foods.all():
            raise forms.ValidationError("Этот тип пищи не подходит для данного вида животного.")
        return food_item

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Количество должно быть больше 0.")
        return quantity

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if cost is not None and cost < 0:
            raise forms.ValidationError("Затраты не могут быть отрицательными.")
        return cost


class FeedingScheduleForm(forms.ModelForm):
    class Meta:
        model = FeedingSchedule
        fields = ['food_item', 'frequency', 'quantity', 'start_date', 'notes']
        widgets = {
            'food_item': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, animal=None, **kwargs):
        super().__init__(*args, **kwargs)
        if animal:
            self.fields['food_item'].queryset = animal.taxonomy.allowed_foods.all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-small'
        self.helper.label_class = ''
        self.helper.layout = Layout(
            Row(Div(Field('food_item', css_class='form-control'),)),
            Row(Div(Field('frequency', css_class='form-control'),)),
            Row(Div(Field('quantity', css_class='form-control'),)),
            Row(Div(Field('start_date', css_class='form-control'),)),
            Row(Div(Field('notes', css_class='form-control'),)),
            FormActions(
                HTML('<button type="submit" class="btn btn-primary mt-2"><i class="bi bi-save"></i> Сохранить расписание</button>'),
                HTML('<button type="button" class="btn btn-secondary mt-2 ms-2" data-bs-dismiss="modal"><i class="bi bi-x-circle"></i> Отмена</button>'),
            ),
        )

    def clean_food_item(self):
        food_item = self.cleaned_data.get('food_item')
        animal = self.instance.animal
        if food_item not in animal.taxonomy.allowed_foods.all():
            raise forms.ValidationError("Этот тип пищи не подходит для данного вида животного.")
        return food_item

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Количество должно быть больше 0.")
        return quantity


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = [
            'name', 'food_type', 'description', 'calcium_content', 'protein_content', 'vitamin_d3_content',
            'requires_calcium', 'requires_vitamin_d3', 'requires_multivitamins'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'food_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'calcium_content': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'protein_content': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vitamin_d3_content': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'requires_calcium': forms.Select(attrs={'class': 'form-control'}),
            'requires_vitamin_d3': forms.Select(attrs={'class': 'form-control'}),
            'requires_multivitamins': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-small'
        self.helper.label_class = ''
        self.helper.layout = Layout(
            Row(Div(Field('name', css_class='form-control'), css_class='col-md-6')),
            Row(Div(Field('food_type', css_class='form-control'), css_class='col-md-6')),
            Row(Div(Field('description', css_class='form-control'), css_class='col-12')),
            Row(
                Div(Field('calcium_content', css_class='form-control'), css_class='col-md-4'),
                Div(Field('protein_content', css_class='form-control'), css_class='col-md-4'),
                Div(Field('vitamin_d3_content', css_class='form-control'), css_class='col-md-4'),
            ),
            Row(
                Div(Field('requires_calcium', css_class='form-control'), css_class='col-md-4'),
                Div(Field('requires_vitamin_d3', css_class='form-control'), css_class='col-md-4'),
                Div(Field('requires_multivitamins', css_class='form-control'), css_class='col-md-4'),
            ),
            FormActions(
                HTML('<button type="submit" class="btn btn-primary mt-2"><i class="bi bi-save"></i> Сохранить</button>'),
                HTML('<a href="{% url \'feeding:food_item_list\' %}" class="btn btn-secondary mt-2 ms-2"><i class="bi bi-x-circle"></i> Отмена</a>'),
            ),
        )


class FeedingRequirementForm(forms.ModelForm):
    class Meta:
        model = FeedingRequirement
        fields = [
            'taxonomy', 'age_group', 'food_type', 'insect_ratio', 'plant_ratio', 'frequency',
            'quantity_per_feeding', 'calcium_frequency', 'vitamin_d3_frequency', 'multivitamin_frequency', 'notes'
        ]
        widgets = {
            'taxonomy': forms.Select(attrs={'class': 'form-control'}),
            'age_group': forms.Select(attrs={'class': 'form-control'}),
            'food_type': forms.Select(attrs={'class': 'form-control'}),
            'insect_ratio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'plant_ratio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'quantity_per_feeding': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'calcium_frequency': forms.Select(attrs={'class': 'form-control'}),
            'vitamin_d3_frequency': forms.Select(attrs={'class': 'form-control'}),
            'multivitamin_frequency': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-small'
        self.helper.label_class = ''
        self.helper.layout = Layout(
            Row(Div(Field('taxonomy', css_class='form-control'), css_class='col-md-6')),
            Row(Div(Field('age_group', css_class='form-control'), css_class='col-md-6')),
            Row(Div(Field('food_type', css_class='form-control'), css_class='col-md-6')),
            Row(
                Div(Field('insect_ratio', css_class='form-control'), css_class='col-md-6'),
                Div(Field('plant_ratio', css_class='form-control'), css_class='col-md-6'),
            ),
            Row(Div(Field('frequency', css_class='form-control'), css_class='col-md-6')),
            Row(Div(Field('quantity_per_feeding', css_class='form-control'), css_class='col-md-6')),
            Row(
                Div(Field('calcium_frequency', css_class='form-control'), css_class='col-md-4'),
                Div(Field('vitamin_d3_frequency', css_class='form-control'), css_class='col-md-4'),
                Div(Field('multivitamin_frequency', css_class='form-control'), css_class='col-md-4'),
            ),
            Row(Div(Field('notes', css_class='form-control'), css_class='col-12')),
            FormActions(
                HTML('<button type="submit" class="btn btn-primary mt-2"><i class="bi bi-save"></i> Сохранить</button>'),
                HTML('<a href="{% url \'feeding:feeding_requirement_list\' %}" class="btn btn-secondary mt-2 ms-2"><i class="bi bi-x-circle"></i> Отмена</a>'),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        insect_ratio = cleaned_data.get('insect_ratio', 0)
        plant_ratio = cleaned_data.get('plant_ratio', 0)
        food_type = cleaned_data.get('food_type')
        if food_type == 'mixed' and (insect_ratio + plant_ratio != 100):
            raise forms.ValidationError("Сумма насекомых и растений должна быть равна 100% для смешанного рациона.")
        if food_type == 'insect' and insect_ratio != 100:
            raise forms.ValidationError("Для насекомоядных животных доля насекомых должна быть 100%.")
        if food_type == 'plant' and plant_ratio != 100:
            raise forms.ValidationError("Для травоядных животных доля растений должна быть 100%.")
        return cleaned_data
