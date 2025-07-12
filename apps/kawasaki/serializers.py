from rest_framework import serializers

from .models import Patient, BloodTest, LiverFunction, Echocardiography, EnrollGroup, InfectiousTest, Samples, CustomTest


class PatientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields = '__all__'
		extra_kwargs = {
			'version': {'required': False, 'read_only': True}
		}

	def validate(self, attrs):
		# For updates, check if version was provided in the request data
		if self.instance:
			request = self.context.get('request')
			if request and hasattr(request, 'data') and 'version' in request.data:
				provided_version = request.data['version']
				if provided_version != self.instance.version:
					raise serializers.ValidationError({
						'version': 'Stale data detected. Please reload and try again.'
					})
		return attrs


class BloodTestSerializer(serializers.ModelSerializer):
	class Meta:
		model = BloodTest
		fields = '__all__'
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


class LiverFunctionSerializer(serializers.ModelSerializer):
	class Meta:
		model = LiverFunction
		fields = '__all__'
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


class EchocardiographySerializer(serializers.ModelSerializer):
	class Meta:
		model = Echocardiography
		fields = '__all__'
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


class EnrollGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = EnrollGroup
		fields = '__all__'


class InfectiousTestSerializer(serializers.ModelSerializer):
	class Meta:
		model = InfectiousTest
		fields = '__all__'
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


class SamplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Samples
        fields = '__all__'
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


class CustomTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTest
        fields = '__all__'
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
