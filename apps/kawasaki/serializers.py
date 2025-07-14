from rest_framework import serializers

from .models import Patient, BloodTest, LiverFunction, Echocardiography, EnrollGroup, InfectiousTest, Samples, CustomTest


class VersionedSerializer(serializers.ModelSerializer):
	class Meta:
		abstract = True
		extra_kwargs = {
			'version': {'required': False, 'read_only': True}
		}

	def validate(self, attrs):
		if self.instance:
			request = self.context.get('request')
			if request and hasattr(request, 'data') and 'version' in request.data:
				provided_version = request.data['version']
				if provided_version != self.instance.version:
					raise serializers.ValidationError({
						'version': 'Stale data detected. Please reload and try again.'
					})
		return attrs

class PatientSerializer(VersionedSerializer):
	creator_name = serializers.CharField(source='creator_full_name', read_only=True)
	modifier_name = serializers.CharField(source='modifier_full_name', read_only=True)

	class Meta(VersionedSerializer.Meta):
		model = Patient
		exclude = ('creator', 'modifier')
		read_only_fields = ('created_at', 'modified_at', 'creator_name', 'modifier_name')
		extra_kwargs = {
			**VersionedSerializer.Meta.extra_kwargs,
		}


class BloodTestSerializer(VersionedSerializer):
	class Meta(VersionedSerializer.Meta):
		model = BloodTest
		fields = '__all__'


class LiverFunctionSerializer(VersionedSerializer):
	class Meta(VersionedSerializer.Meta):
		model = LiverFunction
		fields = '__all__'


class EchocardiographySerializer(VersionedSerializer):
	class Meta(VersionedSerializer.Meta):
		model = Echocardiography
		fields = '__all__'


class EnrollGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = EnrollGroup
		fields = '__all__'


class InfectiousTestSerializer(VersionedSerializer):
	class Meta(VersionedSerializer.Meta):
		model = InfectiousTest
		fields = '__all__'


class SamplesSerializer(VersionedSerializer):
    class Meta(VersionedSerializer.Meta):
        model = Samples
        fields = '__all__'


class CustomTestSerializer(VersionedSerializer):
    class Meta(VersionedSerializer.Meta):
        model = CustomTest
        fields = '__all__'
