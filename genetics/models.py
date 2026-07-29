from django.db import models


class Gene(models.Model):
    INHERITANCE_CHOICES = [
        ('DOMINANT', 'Домinant'),
        ('RECESSIVE', 'Рецессивный'),
        ('CODOMINANT', 'Кодominant'),
    ]
    name = models.CharField('Название', max_length=100, unique=True)
    inheritance_type = models.CharField(max_length=20, choices=INHERITANCE_CHOICES)

    class Meta:
        verbose_name = 'Ген'
        verbose_name_plural = 'Гены'

    def __str__(self):
        return self.name


class MorphGene(models.Model):
    GENOTYPE_CHOICES = [
        ('HET', 'Гетero'),
        ('HOM', 'Гомо'),
        ('SUPER', 'Super'),
    ]
    morph = models.ForeignKey('animals.Morph', on_delete=models.CASCADE, related_name='genes')
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    genotype = models.CharField(max_length=10, choices=GENOTYPE_CHOICES, default='HET')

    class Meta:
        unique_together = ('morph', 'gene')

    def __str__(self):
        return f'{self.morph.name} — {self.gene.name} ({self.genotype})'
