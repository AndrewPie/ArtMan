from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

# from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from django.urls import resolve

from cargo_spec.models import Specification, CargoContent, SpecificationDocument
from cargo_spec.forms import SpecificationForm, CargoContentForm, CargoContentFormSet, SingleSpecificationDocumentForm, MultipleSpecificationDocumentForm
from cargo_spec.utils import specification_marking, check_scan_file


class MyListView(LoginRequiredMixin, ListView):
    model = Specification
    template_name = 'cargo_spec/my_lists.html'
    ordering = ['-marking']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        owner_ = self.request.user
        return queryset.filter(owner = owner_)


class AddSpecificationView(LoginRequiredMixin, CreateView):
    model = Specification
    template_name = 'cargo_spec/specification_form.html'
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
    template_name = 'cargo_spec/specification_form.html'
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
    template_name = 'cargo_spec/specification_detail.html'
    
    def get(self, request, *args, **kwargs):
        context = super(SpecificationDetailView, self).get(request, *args, **kwargs)
        if (self.object.owner != self.request.user) or (self.object.approved is False):
            # return HttpResponseForbidden('Nie masz dostępu do specyfikacji innych użytkowników')
            raise PermissionDenied()
        return context


class SpecificationScanUploadView(LoginRequiredMixin, View):
    template_name = 'cargo_spec/file_upload.html'
    form_class = SingleSpecificationDocumentForm

    def get(self, request, *args, **kwargs):
        spec = Specification.objects.get(pk=self.kwargs['pk'])
        if (spec.owner != self.request.user) or (check_scan_file(spec.marking)):
            raise PermissionDenied()
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            spec = get_object_or_404(Specification, pk=self.kwargs['pk'])
            form.instance.file_type = resolve(request.path_info).url_name
            form.instance.specification = spec
            owner = self.request.user
            form.instance.uploaded_by = owner
            form.save()
            return redirect('cargo_spec:spec-detail', spec.pk)
        else:
            return render(request, self.template_name, {'form': form})
            
            
class SpecificationPhotoUploadView(LoginRequiredMixin, View):
    template_name = 'cargo_spec/file_upload.html'
    form_class = MultipleSpecificationDocumentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            spec = get_object_or_404(Specification, pk=self.kwargs['pk'])
            owner = self.request.user
            for doc in files:
                SpecificationDocument.objects.create(
                    description = form.cleaned_data['description'],
                    document = doc,
                    uploaded_by = owner,
                    specification = spec
                )
            return redirect('cargo_spec:spec-detail', self.kwargs['pk'])
        else:
            return render(request, self.template_name, {'form': form})
            
            
class DeleteSpecificationDocumentView(LoginRequiredMixin, DeleteView):
    model = SpecificationDocument
    
    def get_success_url(self):
        spk = self.kwargs['spk']
        return reverse_lazy('cargo_spec:spec-detail', kwargs={'pk': spk})