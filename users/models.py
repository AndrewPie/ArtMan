from django.db import models
from django.contrib.auth.models import AbstractUser,Group


class User(AbstractUser):

# przykladowy wyglad modelu wraz z pozwoleniami
# ustalic ,jak ma to ostatecznie wygladac

    MEDICAL_SECTION   =0
    TECHNICAL_SECTION =1
    SUPPLY_SECTION    =2
    ADMINISTRATION    =3

    USER_TYPE_CHOICES = (
      (MEDICAL_SECTION, 'medical section'),
      (TECHNICAL_SECTION, 'technical section'),
      (SUPPLY_SECTION, 'supply section'),
      (ADMINISTRATION,'administration')
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

# dodac kierownik , administrator cos z wyzszymi uprawnieniami

# widok do specyfikacji ladunkowej, wyswietla wszystkie listy zaakceptowane
# #lista kart ladunkowych
# 1. Dla statku lista cargo
#    - plik csv
#    - zawiera pola:
#        - identyfikator skrzyni/beczki/przystyłki
#        - krótki opis po angielsku - co to jest
#        - warunki przechowywania
#        - wagę w tonach
#        - objętość w m^3
#        - wymiary
# 2. Dla UC i Instytutu
#    - zbiór plików - pojedynczy katalog
#    - zawiera pliki:
#        - [identyfikator skrzyni/beczki/przystyłki].(xls|xlsx|ods)- bazowy plik z danymi
#        - [identyfikator skrzyni/beczki/przystyłki].pdf - podpisany wydruk
#       #  - [identyfikator skrzyni/beczki/przystyłki]_[n].jpg - zdjęcia ładunku