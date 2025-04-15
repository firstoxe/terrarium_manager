import django_tables2 as tables
from django.conf.urls.static import static

from .models import Animal, Action, Taxonomy
from django.utils.html import format_html


class AnimalTable(tables.Table):
    photo = tables.TemplateColumn(
        template_code='''
            {% if record.photo %}
                <img src="{{ record.photo.url }}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">
            {% else %}
                <div style="width: 50px; height: 50px; background-color: #e9ecef; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: #6c757d;">
                    Нет фото
                </div>
            {% endif %}
            ''',
        verbose_name="Фото",
        orderable=False,
    )
    name = tables.Column(verbose_name="Кличка")
    taxonomy = tables.Column(accessor='taxonomy.scientific_name', verbose_name="Таксон")
    morph = tables.Column(verbose_name="Морфа", empty_values=())
    birth_date = tables.DateColumn(format="d.m.Y", verbose_name="Дата рождения")
    age = tables.Column(verbose_name="Возраст", empty_values=(), orderable=False)
    habitat = tables.TemplateColumn(
        template_code='''
            {% if record.habitat == "tropical" %}
                <span class="badge bg-success">{{ record.get_habitat_display }}</span>
            {% elif record.habitat == "desert" %}
                <span class="badge bg-warning">{{ record.get_habitat_display }}</span>
            {% elif record.habitat == "forest" %}
                <span class="badge bg-primary">{{ record.get_habitat_display }}</span>
            {% else %}
                <span class="badge bg-secondary">{{ record.get_habitat_display }}</span>
            {% endif %}
            ''',
        verbose_name="Среда обитания",
    )
    care_level = tables.TemplateColumn(
        template_code='''
            {% if record.care_level == "easy" %}
                <span class="badge bg-success">{{ record.get_care_level_display }}</span>
            {% elif record.care_level == "medium" %}
                <span class="badge bg-warning">{{ record.get_care_level_display }}</span>
            {% elif record.care_level == "hard" %}
                <span class="badge bg-danger">{{ record.get_care_level_display }}</span>
            {% else %}
                <span class="badge bg-secondary">{{ record.get_care_level_display }}</span>
            {% endif %}
            ''',
        verbose_name="Сложность ухода",
    )
    last_feeding = tables.DateTimeColumn(format="d.m.Y H:i", verbose_name="Последнее кормление", empty_values=())
    overdue_feeding = tables.TemplateColumn(
        template_code='''
            {% if record.overdue_feeding %}
                <span class="badge bg-danger">Пора кормить!</span>
            {% else %}
                <span class="badge bg-success">Всё в порядке</span>
            {% endif %}
            ''',
        verbose_name="Статус кормления",
        orderable=False,
    )
    actions = tables.TemplateColumn(
        template_code='''
            <div class="d-flex gap-1">
                <a href="{% url 'animals:animal_detail' record.pk %}" class="btn btn-sm btn-primary" title="Просмотреть">
                    <i class="bi bi-eye"></i>
                </a>
                <a href="{% url 'animals:animal_update' record.pk %}" class="btn btn-sm btn-warning" title="Редактировать">
                    <i class="bi bi-pencil"></i>
                </a>
                <a href="{% url 'animals:animal_delete' record.pk %}" class="btn btn-sm btn-danger" title="Удалить">
                    <i class="bi bi-trash"></i>
                </a>
                <a href="{% url 'feeding:feeding_event_create' record.pk %}" class="btn btn-sm btn-success" title="Добавить кормление">
                    <i class="bi bi-plus-lg"></i>
                </a>
            </div>
            ''',
        verbose_name="Действия",
        orderable=False,
    )

    # def render_photo(self, value):
    #     return format_html(
    #         '<div class="table-photo" style="background-image: url({})"></div>',
    #         value.url if value else static('img/default-animal.png')
    #     )
    #
    # def render_birth_date(self, value):
    #     return value.strftime("%d.%m.%Y") if value else "—"
    #
    def render_morph(self, record):
        return record.morph.name if record.morph else "-"
    #
    # def render_habitat(self, record):
    #     return record.get_habitat_display()

    def render_last_feeding(self, record):
        return record.last_feeding if record.last_feeding else "Нет данных"

    class Meta:
        model = Animal
        fields = ('photo', 'name', 'taxonomy', 'morph', 'birth_date', 'habitat', 'actions')
        attrs = {'class': 'table table-hover'}
        row_attrs = {
            'class': 'clickable-row',
            'data-href': lambda record: record.get_absolute_url()
        }


class ActionTable(tables.Table):
    description = tables.Column(verbose_name="Описание", attrs={"td": {"style": "white-space: normal;"}})
    actions = tables.TemplateColumn(
        template_code='''
            <a href="{% url 'animals:action_delete' record.animal.pk record.pk %}" class="btn btn-sm btn-danger">
                <i class="bi bi-trash"></i>
            </a>
            ''',
        verbose_name="Действия",
        orderable=False,
    )

    class Meta:
        model = Action
        template_name = "django_tables2/bootstrap5.html"
        fields = ("date", "action_type", "description", "cost", "actions")
        attrs = {"class": "table table-hover", "id": "actions-table"}
        order_by = ("-date",)

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
