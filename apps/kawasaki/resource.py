from import_export.resources import ModelResource

from .models import Patient, BloodTest, LiverFunction, Echocardiography, OtherTest, Samples


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


class OtherTestResource(ModelResource):

    class Meta:
        model = OtherTest


class SamplesResource(ModelResource):

    class Meta:
        model = Samples

