from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from datetime import datetime

from .models import Specification, CargoContent
from .forms import SpecificationForm, CargoContentForm, CargoContentFormSet
from .utils import specification_marking


class MyListView(ListView):
    model = Specification
    template_name = 'my_lists.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        owner_ = self.request.user
        return queryset.filter(owner = owner_)


class AddSpecificationView(CreateView):
    model = Specification
    template_name = 'specification-form.html'
    form_class = SpecificationForm
    
    def get_context_data(self, **kwargs):
        data = super(AddSpecificationView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['cargos'] = CargoContentFormSet(self.request.POST)
        else:
            data['cargos'] = CargoContentFormSet()
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        cargos = context['cargos']
        with transaction.atomic():
            form.instance.owner = self.request.user
            form.instance.marking = specification_marking(form)
            
            self.object = form.save()
            if cargos.is_valid():
                cargos.instance = self.object
                cargos.save()
        return super(AddSpecificationView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('cargo_spec:my-lists')
    
    
class ModifySpecificationView(UpdateView):
    model = Specification
    template_name = 'specification-form.html'
    form_class = SpecificationForm
    
    def get_context_data(self, **kwargs):
        data = super(ModifySpecificationView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['cargos'] = CargoContentFormSet(self.request.POST, instance=self.object)
        else:
            data['cargos'] = CargoContentFormSet(instance=self.object)
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        cargos = context['cargos']
        with transaction.atomic():
            self.object = form.save()
            if cargos.is_valid():
                cargos.instance = self.object
                cargos.save()
        return super(ModifySpecificationView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('cargo_spec:my-lists')