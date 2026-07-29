"""Load species catalog from JSON and import entries into the database on demand."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from django.conf import settings
from django.db import transaction

from animals.models import CareRequirement, Morph, Taxonomy


def get_library_path(kind: str = 'catalog') -> Path:
    """
    kind:
      - 'popular' — виды, которые сразу импортируем в БД
      - 'catalog' — полный справочник, который пользователь выбирает по необходимости
    """
    base_default = settings.BASE_DIR / 'data' / 'species_library_ru.json'
    if kind == 'popular':
        return Path(getattr(settings, 'SPECIES_LIBRARY_POPULAR_PATH', getattr(settings, 'SPECIES_LIBRARY_PATH', base_default)))
    return Path(getattr(settings, 'SPECIES_LIBRARY_CATALOG_PATH', getattr(settings, 'SPECIES_LIBRARY_PATH', base_default)))


@lru_cache(maxsize=2)
def load_library(kind: str = 'catalog') -> dict[str, Any]:
    path = get_library_path(kind=kind)
    with path.open(encoding='utf-8') as fh:
        return json.load(fh)


def clear_library_cache() -> None:
    load_library.cache_clear()


def list_entries(kind: str = 'catalog') -> list[dict[str, Any]]:
    return load_library(kind=kind).get('species', [])


def get_entry(library_id: str, kind: str = 'catalog') -> dict[str, Any] | None:
    for entry in list_entries(kind=kind):
        if entry['id'] == library_id:
            return entry
    return None


def search_entries(
    query: str = '',
    tag: str = '',
    kind: str = 'catalog',
    care_level: str = '',
) -> list[dict[str, Any]]:
    query = query.strip().lower()
    tag = tag.strip().lower()
    care_level = care_level.strip().upper()
    results = []
    for entry in list_entries(kind=kind):
        if tag and tag not in [t.lower() for t in entry.get('tags', [])]:
            continue
        if care_level and entry.get('care_level', '').upper() != care_level:
            continue
        if query:
            haystack = ' '.join([
                entry.get('common_name', ''),
                entry.get('scientific_name', ''),
                entry.get('species', ''),
                entry.get('genus', ''),
            ]).lower()
            if query not in haystack:
                continue
        results.append(entry)
    return results


def is_imported(library_id: str) -> bool:
    return Taxonomy.objects.filter(library_id=library_id).exists()


def get_imported_taxonomy(library_id: str) -> Taxonomy | None:
    return Taxonomy.objects.filter(library_id=library_id).first()


@transaction.atomic
def import_entry(library_id: str, kind: str = 'catalog') -> Taxonomy:
    """Импортирует один вид из справочника (taxon, базовый уход, морфы)."""
    entry = get_entry(library_id, kind=kind)
    if entry is None:
        raise ValueError(f'Unknown library id: {library_id}')

    taxonomy_defaults = {
        'class_name': entry.get('class_name', ''),
        'order': entry.get('order', ''),
        'family': entry.get('family', ''),
        'genus': entry.get('genus', ''),
        'species': entry['species'],
        'subspecies': entry.get('subspecies', ''),
        'scientific_name': entry['scientific_name'],
        'common_name': entry.get('common_name', ''),
        'is_global': True,
    }

    taxonomy = (
        Taxonomy.objects.filter(library_id=library_id).first()
        or Taxonomy.objects.filter(scientific_name=entry['scientific_name']).first()
    )
    if taxonomy:
        for key, value in taxonomy_defaults.items():
            setattr(taxonomy, key, value)
        taxonomy.library_id = library_id
        taxonomy.save()
    else:
        taxonomy = Taxonomy.objects.create(library_id=library_id, **taxonomy_defaults)

    care = entry.get('care')
    if care:
        # Сохраняем остальную структуру справочника как JSON, чтобы не раздувать модель.
        # В дальнейшем из этих данных можно строить UI: размеры террариума, группы/пол, кормление по возрасту и т.д.
        catalog_details = {k: v for k, v in entry.items() if k != 'morphs'}
        CareRequirement.objects.update_or_create(
            taxonomy=taxonomy,
            defaults={**care, 'catalog_details': catalog_details},
        )

    for morph_data in entry.get('morphs', []):
        Morph.objects.get_or_create(
            taxonomy=taxonomy,
            name=morph_data['name'],
            defaults={'description': morph_data.get('description', '')},
        )

    return taxonomy


def import_popular() -> int:
    """Импортирует «популярные» виды в базу (для быстрого старта)."""
    count = 0
    for entry in list_entries(kind='popular'):
        import_entry(entry['id'], kind='popular')
        count += 1
    return count


def import_catalog() -> int:
    """Импортирует полный каталог (обычно для админов/тестовых стендов)."""
    count = 0
    for entry in list_entries(kind='catalog'):
        import_entry(entry['id'], kind='catalog')
        count += 1
    return count
