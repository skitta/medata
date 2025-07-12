from import_export.resources import ModelResource

from .models import Patient, BloodTest, LiverFunction, Echocardiography, InfectiousTest, Samples, CustomTest


class PatientResource(ModelResource):

    class Meta:
        model = Patient


class BloodTestResource(ModelResource):

    class Meta:
        model = BloodTest


class LiverFunctionResource(ModelResource):

    class Meta:
        model = LiverFunction


class EchocardiographyResource(ModelResource):

    class Meta:
        model = Echocardiography


class InfectiousTestResource(ModelResource):

    class Meta:
        model = InfectiousTest


class SamplesResource(ModelResource):

    class Meta:
        model = Samples


class CustomTestResource(ModelResource):

    class Meta:
        model = CustomTest
