from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

# from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from .models import Specification, CargoContent
from .forms import SpecificationForm, CargoContentForm, CargoContentFormSet
from .utils import specification_marking


class MyListView(LoginRequiredMixin, ListView):
    model = Specification
    template_name = 'my_lists.html'
    ordering = ['-marking']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        owner_ = self.request.user
        return queryset.filter(owner = owner_)


class AddSpecificationView(LoginRequiredMixin, CreateView):
    model = Specification
    template_name = 'specification_form.html'
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

            # Sprawdza czy wszystkie wymagane pola dla modelu CargoContent są wypełnione, jeśli nie, to zwraca formularz
            if cargos.is_valid() == False:
                return self.render_to_response(self.get_context_data(form=form, cargos=cargos))

            if cargos.is_valid():
                cargos.instance = self.object
                cargos.save()
        return super(AddSpecificationView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('cargo_spec:my-lists')
    
    
class ModifySpecificationView(LoginRequiredMixin, UpdateView):
    model = Specification
    template_name = 'specification_form.html'
    form_class = SpecificationForm
    
    def get_context_data(self, **kwargs):
        data = super(ModifySpecificationView, self).get_context_data(**kwargs)
        
        if (self.object.owner != self.request.user) or (self.object.approved is True):
            raise PermissionDenied()
            
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
            
            # Sprawdza czy wszystkie wymagane pola dla modelu CargoContent są wypełnione, jeśli nie, to zwraca formularz
            if cargos.is_valid() == False:
                return self.render_to_response(self.get_context_data(form=form, cargos=cargos))
            
            if cargos.is_valid():
                cargos.instance = self.object
                cargos.save()
        return super(ModifySpecificationView, self).form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('cargo_spec:my-lists')
    

class AcceptSpecificationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        spec = get_object_or_404(Specification, pk=pk)
        spec.approved = True
        spec.save()
        
        return redirect('cargo_spec:spec-detail', spec.pk)
    
    
class DeleteSpecificationView(LoginRequiredMixin, DeleteView):
    model = Specification
    
    def get_success_url(self):
        return reverse_lazy('cargo_spec:my-lists')
    
    
class SpecificationDetailView(LoginRequiredMixin, DetailView):
    model = Specification
    template_name = 'specification_detail.html'
    
    def get(self, request, *args, **kwargs):
        context = super(SpecificationDetailView, self).get(request, *args, **kwargs)
        if (self.object.owner != self.request.user) or (self.object.approved is False):
            # return HttpResponseForbidden('Nie masz dostępu do specyfikacji innych użytkowników')
            raise PermissionDenied()
        return context
