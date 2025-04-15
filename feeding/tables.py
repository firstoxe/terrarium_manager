import django_tables2 as tables
from .models import FeedingEvent, FeedingSchedule, FoodItem, FeedingRequirement


class FeedingEventTable(tables.Table):
    date = tables.Column(verbose_name="Дата")
    food_item = tables.Column(verbose_name="Тип пищи")
    quantity = tables.Column(verbose_name="Количество")
    cost = tables.Column(verbose_name="Стоимость")
    used_calcium = tables.BooleanColumn(verbose_name="Кальций", yesno="✔,✘")
    used_vitamin_d3 = tables.BooleanColumn(verbose_name="Витамин D3", yesno="✔,✘")
    used_multivitamins = tables.BooleanColumn(verbose_name="Мультивитамины", yesno="✔,✘")
    actions = tables.TemplateColumn(
        template_code='''
            <a href="{% url 'feeding:feeding_event_delete' record.animal.pk record.pk %}" class="btn btn-sm btn-danger">
                <i class="bi bi-trash"></i>
            </a>
            ''',
        verbose_name="Действия",
        orderable=False,
    )

    class Meta:
        model = FeedingEvent
        template_name = "django_tables2/bootstrap5.html"
        fields = (
        "date", "food_item", "quantity", "cost", "used_calcium", "used_vitamin_d3", "used_multivitamins", "actions")
        attrs = {"class": "table table-hover", "id": "feeding-events-table"}
        order_by = ("-date",)

    def render_date(self, value):
        return value.strftime("%d.%m.%Y %H:%M")

    def render_food_item(self, record):
        return f"{record.food_item.name} ({record.food_item.get_food_type_display()})"

    def render_cost(self, value):
        return f"{value} р." if value else "-"


class FeedingScheduleTable(tables.Table):
    food_item = tables.Column(verbose_name="Тип пищи")
    frequency = tables.Column(verbose_name="Частота")
    quantity = tables.Column(verbose_name="Количество")
    start_date = tables.Column(verbose_name="Дата начала")
    notes = tables.Column(verbose_name="Заметки")
    actions = tables.TemplateColumn(
        template_code='''
            <a href="{% url 'feeding:feeding_schedule_delete' record.animal.pk record.pk %}" class="btn btn-sm btn-danger">
                <i class="bi bi-trash"></i>
            </a>
            ''',
        verbose_name="Действия",
        orderable=False,
    )

    class Meta:
        model = FeedingSchedule
        template_name = "django_tables2/bootstrap5.html"
        fields = ("food_item", "frequency", "quantity", "start_date", "notes", "actions")
        attrs = {"class": "table table-hover", "id": "feeding-schedule-table"}

    def render_food_item(self, record):
        return f"{record.food_item.name} ({record.food_item.get_food_type_display()})"

    def render_frequency(self, record):
        return record.get_frequency_display()

    def render_start_date(self, value):
        return value.strftime("%d.%m.%Y")

    def render_notes(self, value):
        return value or "-"


class FeedingRecommendationTable(tables.Table):
    food_type = tables.Column(verbose_name="Тип пищи")
    insect_ratio = tables.Column(verbose_name="Насекомые (%)")
    plant_ratio = tables.Column(verbose_name="Растения (%)")
    frequency = tables.Column(verbose_name="Частота")
    quantity_per_feeding = tables.Column(verbose_name="Количество за кормление")
    calcium_frequency = tables.Column(verbose_name="Кальций")
    vitamin_d3_frequency = tables.Column(verbose_name="Витамин D3")
    multivitamin_frequency = tables.Column(verbose_name="Мультивитамины")
    actions = tables.TemplateColumn(
        template_code='''
            {% if record.food_type == "unknown" %}
            <a href="{% url 'feeding:feeding_requirement_create' %}" class="btn btn-sm btn-success">
                <i class="bi bi-plus-lg"></i> Добавить требования
            </a>
            {% endif %}
            ''',
        verbose_name="Действия",
        orderable=False,
    )

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        fields = ("food_type", "insect_ratio", "plant_ratio", "frequency", "quantity_per_feeding", "calcium_frequency",
                  "vitamin_d3_frequency", "multivitamin_frequency", "actions")
        attrs = {"class": "table table-hover", "id": "feeding-recommendation-table"}


class FoodItemTable(tables.Table):
    actions = tables.TemplateColumn(
        template_code='''
        <a href="{% url 'feeding:food_item_update' record.pk %}" class="btn btn-sm btn-warning">
            <i class="bi bi-pencil"></i>
        </a>
        <a href="{% url 'feeding:food_item_delete' record.pk %}" class="btn btn-sm btn-danger">
            <i class="bi bi-trash"></i>
        </a>
        ''',
        verbose_name="Действия",
        orderable=False,
    )

    class Meta:
        model = FoodItem
        template_name = "django_tables2/bootstrap5.html"
        fields = ("name", "food_type", "calcium_content", "protein_content", "vitamin_d3_content", "requires_calcium", "requires_vitamin_d3", "requires_multivitamins")
        attrs = {"class": "table table-hover"}

    def render_food_type(self, record):
        return record.get_food_type_display()

    def render_calcium_content(self, value):
        return f"{value} мг/кг" if value else "-"

    def render_protein_content(self, value):
        return f"{value} г/кг" if value else "-"

    def render_vitamin_d3_content(self, value):
        return f"{value} МЕ/кг" if value else "-"

    def render_requires_calcium(self, record):
        return record.get_requires_calcium_display()

    def render_requires_vitamin_d3(self, record):
        return record.get_requires_vitamin_d3_display()

    def render_requires_multivitamins(self, record):
        return record.get_requires_multivitamins_display()


class FeedingRequirementTable(tables.Table):
    actions = tables.TemplateColumn(
        template_code='''
        <a href="{% url 'feeding:feeding_requirement_update' record.pk %}" class="btn btn-sm btn-warning">
            <i class="bi bi-pencil"></i>
        </a>
        <a href="{% url 'feeding:feeding_requirement_delete' record.pk %}" class="btn btn-sm btn-danger">
            <i class="bi bi-trash"></i>
        </a>
        ''',
        verbose_name="Действия",
        orderable=False,
    )

    class Meta:
        model = FeedingRequirement
        template_name = "django_tables2/bootstrap5.html"
        fields = ("taxonomy", "age_group", "food_type", "insect_ratio", "plant_ratio", "frequency", "quantity_per_feeding", "calcium_frequency", "vitamin_d3_frequency", "multivitamin_frequency")
        attrs = {"class": "table table-hover"}

    def render_taxonomy(self, record):
        return record.taxonomy.scientific_name

    def render_age_group(self, record):
        return record.get_age_group_display()

    def render_food_type(self, record):
        return record.get_food_type_display()

    def render_frequency(self, record):
        return record.get_frequency_display()

    def render_calcium_frequency(self, record):
        return record.get_calcium_frequency_display()

    def render_vitamin_d3_frequency(self, record):
        return record.get_vitamin_d3_frequency_display()

    def render_multivitamin_frequency(self, record):
        return record.get_multivitamin_frequency_display()
