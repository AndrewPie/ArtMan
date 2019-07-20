from django.db import models
from django.contrib.auth.models import AbstractUser,Group


class User(AbstractUser):

    MEDICAL_SECTION =0
    TECHNICAL_SECTION=1
    SUPPLY_SECTION=2
    
    USER_TYPE_CHOICES = (
      (MEDICAL_SECTION, 'medical section'),
      (TECHNICAL_SECTION, 'technical section'),
      (SUPPLY_SECTION, 'supply section'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,null=True)
    class Meta:
        permissions = [
                ("Medical_section_add_report", "Can add medical report"),
                ("Medical_section_del_report", "Can del medical report"),
                ("Medical_section_change_report", "Can change medical report"),
                ("technical_section_add_report", "Can add technical report"),
                ("technical_section_del_report", "Can del technical report"),
                ("technical_section_change_report", "Can change technical report"),
                ("supply_section_add_report", "Can add supply report"),
                ("supply_section_del_report", "Can del supply report"),
                ("supply_section_change_report", "Can change supply report"),
            ]

