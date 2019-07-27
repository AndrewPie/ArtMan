from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction


from datetime import datetime


from report.models import Report, Section, Note
from report.forms import NoteForm, SectionForm


class ReportContentView(LoginRequiredMixin, DetailView):
    template_name = 'report/report_contents_page.html'

    def get_object(self):
        year_ = datetime.now().year
        month_ = datetime.now().month
        return get_object_or_404(Report, year=year_, month=month_)


class NoteView(LoginRequiredMixin, CreateView):
    form_class = NoteForm
    template_name = 'report/notes.html'

    def get_context_data(self, **kwargs):
        data = super(NoteView, self).get_context_data(**kwargs)
        section_ = get_object_or_404(Section, pk=self.kwargs.get('pk'))
        data['section'] = section_
        data['note_list'] = Note.objects.filter(section=section_).order_by('pk')
        return data
        
    def form_valid(self, form):
        context = self.get_context_data()
        section = context['section']
        with transaction.atomic():
            form.instance.section = section
            self.object = form.save()
        return super(NoteView, self).form_valid(form)
        
    def get_success_url(self):
        context = self.get_context_data()
        section = context['section']
        return reverse_lazy('report:note-list', kwargs={'pk': section.pk})


class AddSectionView(CreateView):
    form_class = SectionForm
    template_name = 'report/add_section.html'
