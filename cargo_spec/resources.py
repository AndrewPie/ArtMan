from import_export import resources, fields

from cargo_spec.models import Specification


class SpecificationResource(resources.ModelResource):
    class Meta:
        model = Specification
        fields = ['marking', 'description', 'storage', 'weight', 'capacity', 'dimension_length', 'dimension_width', 'dimension_height']
        export_order = fields

    def get_queryset(self):
        return self._meta.model.objects.filter(approved=True)

    def dehydrate_weight(self, specification):
        return f'{ specification.weight * 10**(-3) }' 