from rest_framework import serializers

from .models import Patient, BloodTest, LiverFunction, Echocardiography


class PatientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields = '__all__'


class BloodTestSerializer(serializers.ModelSerializer):
	class Meta:
		model = BloodTest
		fields = '__all__'


class LiverFunctionSerializer(serializers.ModelSerializer):
	class Meta:
		model = LiverFunction
		fields = '__all__'


class EchocardiographySerializer(serializers.ModelSerializer):
	class Meta:
		model = Echocardiography
		fields = '__all__'
