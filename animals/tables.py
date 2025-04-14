import django_tables2 as tables
from django.conf.urls.static import static

from .models import Animal, Action, Taxonomy
from django.utils.html import format_html


class AnimalTable(tables.Table):
    photo = tables.TemplateColumn(
        '<img src="{% if record.photo %}{{ record.photo.url }}{% else %}/static/no-image.png{% endif %}" class="animal-thumbnail">',
        verbose_name="Фото"
    )
    name = tables.Column(verbose_name="Кличка")
    taxonomy = tables.Column(accessor='taxonomy.scientific_name', verbose_name="Таксон")
    morph = tables.Column(verbose_name="Морфа", empty_values=())
    birth_date = tables.DateColumn(format="d.m.Y", verbose_name="Дата рождения")
    habitat = tables.Column(verbose_name="Среда обитания")
    actions = tables.TemplateColumn(
        """<div class="btn-group">
    <a href="{% url 'animals:animal_detail' record.pk %}"
       class="btn btn-sm btn-outline-primary"
       title="Просмотр">
        <i class="bi bi-eye"></i>
    </a>
    <a href="{% url 'animals:animal_update' record.pk %}"
       class="btn btn-sm btn-outline-warning"
       title="Редактировать">
        <i class="bi bi-pencil"></i>
    </a>
    <a href="{% url 'animals:animal_delete' record.pk %}"
       class="btn btn-sm btn-outline-danger"
       title="Удалить">
        <i class="bi bi-trash"></i>
    </a>
</div>""",
        verbose_name="Действия",
        orderable=False
    )

    def render_photo(self, value):
        return format_html(
            '<div class="table-photo" style="background-image: url({})"></div>',
            value.url if value else static('img/default-animal.png')
        )

    def render_birth_date(self, value):
        return value.strftime("%d.%m.%Y") if value else "—"

    def render_morph(self, record):
        return record.morph.name if record.morph else "-"

    def render_habitat(self, record):
        return record.get_habitat_display()

    class Meta:
        model = Animal
        fields = ('photo', 'name', 'taxonomy', 'morph', 'birth_date', 'habitat', 'actions')
        attrs = {'class': 'table table-hover'}
        row_attrs = {
            'class': 'clickable-row',
            'data-href': lambda record: record.get_absolute_url()
        }


class ActionTable(tables.Table):
    date = tables.Column(verbose_name="Дата")
    action_type = tables.Column(verbose_name="Тип")
    description = tables.Column(verbose_name="Описание")
    cost = tables.Column(verbose_name="Затраты")

    class Meta:
        model = Action
        template_name = "django_tables2/bootstrap5.html"
        fields = ("date", "action_type", "description", "cost")
        attrs = {"class": "table table-hover", "id": "actions-table"}
        order_by = ("-date",)  # Сортировка по дате по убыванию

    def render_date(self, value):
        return value.strftime("%d.%m.%Y %H:%M")

    def render_action_type(self, record):
        return record.get_action_type_display()

    def render_cost(self, value):
        return f"{value} р." if value else "-"


class TaxonomyTable(tables.Table):
    actions = tables.TemplateColumn(
        template_code='''
        <a href="{% url 'animals:taxonomy_update' record.pk %}" class="btn btn-sm btn-warning">
            <i class="bi bi-pencil"></i>
        </a>
        <a href="{% url 'animals:taxonomy_delete' record.pk %}" class="btn btn-sm btn-danger">
            <i class="bi bi-trash"></i>
        </a>
        ''',
        verbose_name="Действия",
        orderable=False,
    )

    class Meta:
        model = Taxonomy
        template_name = "django_tables2/bootstrap5.html"
        fields = ("class_name", "order", "family", "genus", "species", "subspecies", "scientific_name")
        attrs = {"class": "table table-hover"}