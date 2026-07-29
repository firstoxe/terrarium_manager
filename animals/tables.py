import django_tables2 as tables

from .models import Animal, Action


class AnimalTable(tables.Table):
    photo = tables.TemplateColumn(
        '{% if record.photo %}<img src="{{ record.photo.url }}" class="animal-thumbnail" alt="">{% else %}<span class="tm-chip">Нет фото</span>{% endif %}',
        verbose_name="Фото"
    )
    name = tables.Column(verbose_name="Кличка")
    taxonomy = tables.Column(accessor='taxonomy__scientific_name', verbose_name="Таксон")
    morph = tables.Column(verbose_name="Морфа", empty_values=())
    birth_date = tables.DateColumn(format="d.m.Y", verbose_name="Дата рождения")
    habitat = tables.Column(verbose_name="Среда обитания")
    actions = tables.TemplateColumn(
        """<div class="btn-group">
    <a href="{% url 'animals:animal_detail' record.pk %}"
       class="btn btn-sm btn-outline-primary"
       title="Просмотр" aria-label="Просмотр {{ record.name }}">
        <i class="bi bi-eye" aria-hidden="true"></i>
    </a>
    <a href="{% url 'animals:animal_update' record.pk %}"
       class="btn btn-sm btn-outline-secondary"
       title="Редактировать" aria-label="Редактировать {{ record.name }}">
        <i class="bi bi-pencil" aria-hidden="true"></i>
    </a>
    <a href="{% url 'animals:animal_delete' record.pk %}"
       class="btn btn-sm btn-outline-danger"
       title="Удалить" aria-label="Удалить {{ record.name }}">
        <i class="bi bi-trash" aria-hidden="true"></i>
    </a>
</div>""",
        verbose_name="Действия",
        orderable=False
    )

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
        order_by = ("-date",)

    def render_date(self, value):
        return value.strftime("%d.%m.%Y %H:%M")

    def render_action_type(self, record):
        return record.get_action_type_display()

    def render_cost(self, value):
        return f"{value} р." if value else "-"
