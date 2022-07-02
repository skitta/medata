from import_export.resources import ModelResource

from .models import Patient


class PatientResource(ModelResource):

    class Meta:
        model = Patient