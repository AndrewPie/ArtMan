from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import resolve, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_weasyprint import WeasyTemplateResponseMixin

from cargo_spec.forms import (
    CargoContentFormSet,
    MultipleSpecificationDocumentForm,
    SingleSpecificationDocumentForm,
    SpecificationForm,
)
from cargo_spec.models import CargoContent, Specification, SpecificationDocument
from cargo_spec.tables import CargoContentTable
from cargo_spec.resources import SpecificationResource
from cargo_spec.utils import check_scan_file, specification_marking


def user_test(self):
    self.object = self.get_object()
    pass_test = [self.request.user.is_staff, self.request.user == self.object.owner]
    return any(pass_test)


class MyListView(LoginRequiredMixin, ListView):
    model = Specification
    template_name = "cargo_spec/my_lists.html"
    ordering = ["-marking"]

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_ = self.request.user
        return queryset.filter(owner=owner_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["a_list"] = [s.approved for s in queryset]
        return context


class AddSpecificationView(LoginRequiredMixin, CreateView):
    model = Specification
    template_name = "cargo_spec/specification_form.html"
    form_class = SpecificationForm

    def get_context_data(self, **kwargs):
        data = super(AddSpecificationView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["cargos"] = CargoContentFormSet(self.request.POST)
        else:
            data["cargos"] = CargoContentFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        cargos = context["cargos"]
        with transaction.atomic():
            form.instance.owner = self.request.user
            form.instance.marking = specification_marking(form)

            self.object = form.save()

            # Sprawdza czy wszystkie wymagane pola dla modelu CargoContent są wypełnione, jeśli nie, to zwraca formularz
            if cargos.is_valid():
                cargos.instance = self.object
                cargos.save()
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, cargos=cargos)
                )

        return super(AddSpecificationView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cargo_spec:my-lists")


class ModifySpecificationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Specification
    template_name = "cargo_spec/specification_form.html"
    form_class = SpecificationForm

    def test_func(self):
        return user_test(self)

    def get_context_data(self, **kwargs):
        data = super(ModifySpecificationView, self).get_context_data(**kwargs)

        if self.object.approved is True:
            raise PermissionDenied()

        if self.request.POST:
            data["cargos"] = CargoContentFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data["cargos"] = CargoContentFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        cargos = context["cargos"]
        with transaction.atomic():

            if "accept_spec" in self.request.POST:
                form.instance.approved = True

            self.object = form.save()

            if cargos.is_valid():
                cargos.instance = self.object
                cargos.save()
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, cargos=cargos)
                )

        return super(ModifySpecificationView, self).form_valid(form)

    def get_success_url(self):
        if self.object.approved is False:
            return reverse_lazy("cargo_spec:my-lists")
        else:
            # FIXME: zrobić przekierowanie do cargo_spec:spec-detail
            return reverse_lazy("cargo_spec:my-lists")


class DeleteSpecificationView(LoginRequiredMixin, DeleteView):
    model = Specification

    def get_success_url(self):
        return reverse_lazy("cargo_spec:my-lists")


# TODO: sprawdzić czy potrzebny jest login i user passes


class SpecificationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Specification
    template_name = "cargo_spec/specification_detail.html"
    # NOTE: uzyskujemy dzięki temu zmianę w template z {{object}} na {{specification}}
    context_object_name = "specification"

    def test_func(self):
        return user_test(self)

    def get(self, request, *args, **kwargs):
        data = super(SpecificationDetailView, self).get(request, *args, **kwargs)
        if self.object.approved is False:
            raise PermissionDenied()
        return data

    def get_context_data(self, **kwargs):
        context = super(SpecificationDetailView, self).get_context_data(**kwargs)
        specification_ = get_object_or_404(Specification, pk=self.kwargs["pk"])
        table = CargoContentTable(
            CargoContent.objects.filter(specification=specification_)
        )
        context["table"] = table
        return context


class SpecificationScanUploadView(LoginRequiredMixin, View):
    template_name = "cargo_spec/file_upload.html"
    form_class = SingleSpecificationDocumentForm

    def get(self, request, *args, **kwargs):
        spec = Specification.objects.get(pk=self.kwargs["pk"])
        if (spec.owner != self.request.user) or (check_scan_file(spec.marking)):
            raise PermissionDenied()
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            spec = get_object_or_404(Specification, pk=self.kwargs["pk"])
            form.instance.file_type = resolve(request.path_info).url_name
            form.instance.specification = spec
            owner = self.request.user
            form.instance.uploaded_by = owner
            form.save()
            return redirect("cargo_spec:spec-detail", spec.pk)
        else:
            return render(request, self.template_name, {"form": form})


class SpecificationPhotoUploadView(LoginRequiredMixin, View):
    template_name = "cargo_spec/file_upload.html"
    form_class = MultipleSpecificationDocumentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        files = request.FILES.getlist("file_field")
        if form.is_valid():
            spec = get_object_or_404(Specification, pk=self.kwargs["pk"])
            owner = self.request.user
            for doc in files:
                SpecificationDocument.objects.create(
                    description=form.cleaned_data["description"],
                    document=doc,
                    uploaded_by=owner,
                    specification=spec,
                )
            return redirect("cargo_spec:spec-detail", self.kwargs["pk"])
        else:
            return render(request, self.template_name, {"form": form})


class DeleteSpecificationDocumentView(LoginRequiredMixin, DeleteView):
    model = SpecificationDocument

    def get_success_url(self):
        spk = self.kwargs["spk"]
        return reverse_lazy("cargo_spec:spec-detail", kwargs={"pk": spk})


class SpecificationPDFView(LoginRequiredMixin, WeasyTemplateResponseMixin, DetailView):
    model = Specification
    template_name = "cargo_spec/specification_to_pdf.html"
    context_object_name = "specification"
    # pdf_attachment = False
    pdf_stylesheets = [
        "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    ]

    def get(self, request, *args, **kwargs):
        context = super(SpecificationPDFView, self).get(request, *args, **kwargs)
        if (self.object.owner != self.request.user) or (self.object.approved is False):
            raise PermissionDenied()
        return context

    def get_context_data(self, **kwargs):
        context = super(SpecificationPDFView, self).get_context_data(**kwargs)
        specification_ = get_object_or_404(Specification, pk=self.kwargs["pk"])
        empty_row_len = range(20 - specification_.cargos_content.all().count())
        context["empty_row_len"] = empty_row_len
        return context

    def get_pdf_filename(self):
        specification_ = get_object_or_404(Specification, pk=self.kwargs["pk"])
        pdf_filename = f"{specification_.marking}.pdf"
        return pdf_filename


class ApprovedSpecificationsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Specification
    template_name = "cargo_spec/approved_specifications.html"
    ordering = ["owner_id"]

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(approved=True)


class SpecificationCsvView(View):
    def get(self, *args, **kwargs):
        dataset = SpecificationResource().export()
        response = HttpResponse(dataset.csv, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="specifications.csv"'
        return response

