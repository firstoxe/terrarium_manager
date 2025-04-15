from django.contrib.auth import get_user_model
from django.db import models
from animals.models import Animal


User = get_user_model()

class FoodItem(models.Model):
    FOOD_TYPES = [
        ('insect', 'Насекомые'),
        ('rodent', 'Грызуны'),
        ('plant', 'Растения'),
        ('commercial', 'Коммерческий корм'),
        ('other', 'Другое'),
    ]
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('every_feeding', 'Каждое кормление'),
        ('weekly', 'Еженедельно'),
        ('biweekly', 'Раз в 2 недели'),
        ('none', 'Не требуется'),
    ]

    name = models.CharField(max_length=100)  # Например, "Сверчки", "Мышь", "Капуста"
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES)
    description = models.TextField(blank=True)
    calcium_content = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # мг/кг
    protein_content = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # г/кг
    vitamin_d3_content = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # МЕ/кг
    requires_calcium = models.CharField(max_length=20, choices=FREQUENCY_CHOICES,
                                        default='none')  # Частота добавления кальция
    requires_vitamin_d3 = models.CharField(max_length=20, choices=FREQUENCY_CHOICES,
                                           default='none')  # Частота добавления витамина D3
    requires_multivitamins = models.CharField(max_length=20, choices=FREQUENCY_CHOICES,
                                              default='none')  # Частота добавления мультивитаминов

    def __str__(self):
        return self.name


class FeedingEvent(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='feeding_events')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Например, 5 сверчков, 1 мышь
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Стоимость
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    requirement = models.ForeignKey('FeedingRequirement', on_delete=models.SET_NULL, null=True)
    used_calcium = models.BooleanField(default=False)
    used_vitamin_d3 = models.BooleanField(default=False)
    used_multivitamins = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.animal.name} - {self.food_item.name} ({self.date})"


class FeedingSchedule(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('biweekly', 'Раз в 2 недели'),
        ('monthly', 'Ежемесячно'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='feeding_schedules')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.animal.name} - {self.food_item.name} ({self.frequency})"


class FeedingRequirement(models.Model):
    AGE_GROUPS = [
        ('newborn', 'Новорождённый (0–6 месяцев)'),
        ('juvenile', 'Ювенильный (6–18 месяцев)'),
        ('adult', 'Взрослый (18+ месяцев)'),
    ]
    FOOD_TYPES = [
        ('insect', 'Насекомые'),
        ('plant', 'Растения'),
        ('rodent', 'Грызуны'),
        ('mixed', 'Смешанный'),
    ]
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('every_other_day', 'Через день'),
        ('every_3_days', 'Каждые 3 дня'),
        ('weekly', 'Еженедельно'),
        ('biweekly', 'Раз в 2 недели'),
    ]
    SUPPLEMENT_FREQUENCY = [
        ('every_feeding', 'Каждое кормление'),
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('biweekly', 'Раз в 2 недели'),
        ('none', 'Не требуется'),
    ]

    taxonomy = models.ForeignKey('animals.Taxonomy', on_delete=models.CASCADE, related_name='feeding_requirements')
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES)
    insect_ratio = models.IntegerField(default=0)  # % насекомых в рационе
    plant_ratio = models.IntegerField(default=0)   # % растений в рационе
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    quantity_per_feeding = models.IntegerField()   # Количество пищи за кормление
    calcium_frequency = models.CharField(max_length=20, choices=SUPPLEMENT_FREQUENCY, default='none')
    vitamin_d3_frequency = models.CharField(max_length=20, choices=SUPPLEMENT_FREQUENCY, default='none')
    multivitamin_frequency = models.CharField(max_length=20, choices=SUPPLEMENT_FREQUENCY, default='none')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.taxonomy.species} ({self.get_age_group_display()})"

