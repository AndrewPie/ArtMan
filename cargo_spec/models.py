import os
from django.contrib import admin

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

class Specification(models.Model):
    STORAGE = (
        ('POKŁAD', 'pokład'),
        ('ŁADOWNIA', 'ładownia'),
        ('KABINA', 'kabina'),
        ('+4', '+4'), 
        ('-20', '-20'),
        ('-80', '-80'),
        ('DOWOLNE', 'dowolne')
)

    marking = models.CharField(unique=True, max_length=64)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    package_type = models.CharField(max_length=64)
    dimension_length = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    dimension_width = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    dimension_height = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    capacity = models.PositiveIntegerField()
    weight =  models.PositiveIntegerField(validators=[MinValueValidator(1)])
    storage = models.CharField(max_length=32, choices=STORAGE)
    description = models.CharField(max_length=128)
    total_value = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    approved = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        capacity_ = self.dimension_length * self.dimension_width * self.dimension_height
        self.capacity = capacity_
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.marking


class CargoContent(models.Model):
    name = models.CharField(max_length=128)
    serial_number = models.CharField(max_length=64, blank=True)
    quantity = models.DecimalField(max_digits=7, decimal_places=1)
    unit_of_measurement = models.CharField(max_length=24)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, related_name='cargos_content')
    
    def __str__(self):
        return f'{self.specification.marking} - {self.name}'
    

def get_upload_path(instance, filename, *args, **kwargs):
    try:
        if instance.file_type == 'scan-upload':
            txt = 'scan'
    except Exception:
        txt = 'photo'
    name = f'{instance.specification.marking}_{txt}_{filename}'
    path = f'cargo_spec/{instance.specification.marking}/{txt}'
    return os.path.join(path, name)

class SpecificationDocument(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=get_upload_path)
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    
    @property
    def filename(self):
        return os.path.basename(self.document.name)

    @property
    def only_file_path(self):
        return os.path.dirname(self.document.name)