import django_tables2 as tables
from django.conf.urls.static import static

from .models import Animal
from django.utils.html import format_html


class AnimalTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='animals/_actions_column.html',
        orderable=False,
        verbose_name=' ',
        attrs={"td": {"class": "text-nowrap actions"}}
    )

    class Meta:
        model = Animal
        fields = ('photo', 'name', 'species', 'sex', 'birth_date')
        attrs = {
            'class': 'table table-hover table-striped grappelli-table',
            'thead': {'class': 'thead-light'}
        }
        row_attrs = {
            'class': 'clickable-row',
            'data-href': lambda record: record.get_absolute_url()
        }

    def render_photo(self, value):
        return format_html(
            '<div class="table-photo" style="background-image: url({})"></div>',
            value.url if value else static('img/default-animal.png')
        )

    def render_birth_date(self, value):
        return value.strftime("%d.%m.%Y") if value else "—"
