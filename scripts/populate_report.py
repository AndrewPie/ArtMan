from report.models import *

def run():
    report = Report()
    report.save()
    
    
    gen = Section()
    gen.report = report
    gen.title = 'Sprawy ogólne'
    gen.save()
    
    tech = Section()
    tech.report = report
    tech.title = 'Sprawozdanie techniczne'
    tech.save()
    
    med = Section()
    med.report = report
    med.title = 'Sprawozdanie medyczne'
    med.save()
    
    
    tech_vehicles=Section()
    tech_vehicles.report = report
    tech_vehicles.section_master = tech
    tech_vehicles.title = 'Park maszynowy'
    tech_vehicles.save()

    tech_repairs=Section()
    tech_repairs.report = report
    tech_repairs.section_master = tech
    tech_repairs.title = 'Naprawy i instalacje'
    tech_repairs.save()

    med_general=Section()
    med_general.report = report
    med_general.section_master = med
    med_general.title = 'Ogólne'
    med_general.save()

    med_unexpected=Section()
    med_unexpected.report = report
    med_unexpected.section_master = med
    med_unexpected.title = 'Przypadki nagłe'
    med_unexpected.save()


    Note.objects.create(title='Sprzątanie magazynów', section=gen)
    Note.objects.create(title='Dyżury kuchenne', section=gen)
    Note.objects.create(title='Obchody techniczne', section=gen)
    
    Note.objects.create(title='Naprawa koparki', section=tech_vehicles)
    Note.objects.create(title='Wymiana oleju w ciągniku', section=tech_vehicles)

    Note.objects.create(title='Wymiana okien w domku letnim nr 2', section=tech_repairs)
    Note.objects.create(title='Wymiana okien w domku letnim nr 3', section=tech_repairs)
    Note.objects.create(title='Instalacja oświetlenia na sali gimnastycznej', section=tech_repairs)
    Note.objects.create(title='Instalacja oświetlenia w stolarni', section=tech_repairs)
    
    Note.objects.create(title='Sprawdzenie terminu medykamentów', section=med_general)
    Note.objects.create(title='Utylizacja przeterminowanych środków', section=med_general)
    
    Note.objects.create(title='Jan Kowalski - udzielono pomocy po zatruciu pokarmowym', section=med_unexpected)

    print('OK')