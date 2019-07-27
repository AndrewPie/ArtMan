from django.db import models
from  django.template.loader import render_to_string
from datetime import datetime


class Report(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    
    class Meta:
        unique_together = ['year', 'month']
        
    def save(self, *args, **kwargs):
        self.year = datetime.now().year
        self.month = datetime.now().month
        super().save(*args, **kwargs)
        
    def get_as_html(self):
        return render_to_string('report/report.html', {'report': self})

    def main_sections(self):
        return self.sections.filter(section_master=None)
        
    def __str__(self):
        return f'Sprawozdanie miesięczne ({self.year}-{self.month})'
    

class Section(models.Model):
    title = models.CharField(max_length=128, unique=True)
    text_entry = models.CharField(max_length=128, blank=True)
    text_end = models.CharField(max_length=128, blank=True)
    section_master = models.ForeignKey('self', related_name='subsections', on_delete=models.CASCADE, blank=True, null=True)
    report = models.ForeignKey(Report, related_name='sections', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        ordering = ['pk']
    
    def __str__(self):
        if self.section_master:
            return f'{self.report.year}/{self.report.month} - {self.section_master.title} - {self.title}'
        return f'{self.report.year}/{self.report.month} - {self.title}'

class Note(models.Model):
    title = models.CharField(max_length=128)
    section = models.ForeignKey(Section, related_name='notes', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.section} - Wpis_id:{self.pk}'