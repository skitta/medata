from calendar import c
import numpy as np
import pandas as pd
import zipfile

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import Http404, HttpResponse, FileResponse

from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from .models import Patient, Echocardiography, BloodTest, LiverFunction, EnrollGroup, InfectiousTest, Samples, CustomTest
from .serializers import PatientSerializer, BloodTestSerializer, LiverFunctionSerializer, EchocardiographySerializer,\
    EnrollGroupSerializer, InfectiousTestSerializer, SamplesSerializer, CustomTestSerializer
from .resource import PatientResource, BloodTestResource, LiverFunctionResource, EchocardiographyResource, \
    InfectiousTestResource, SamplesResource, CustomTestResource
from . import signals


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        if not isinstance(validated_data, dict):
            return Response(
                {'error': 'Authentication failed - invalid response format'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        if 'user' not in validated_data:
            return Response(
                {'error': 'Authentication failed - user not found in response'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Get full name without space
        full_name = f"{user.first_name}{user.last_name}".strip()

        return Response({
            'token': token.key,
            'full_name': full_name or user.username
        })


class OptimisticLockingViewSet(viewsets.ModelViewSet):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_update(serializer)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)

        # Return the updated instance with new version
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PatientViewSet(OptimisticLockingViewSet):
    queryset = Patient.objects.all().order_by('id')
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['=registered_ID', 'full_name']
    filterset_fields = {
        'group': ['exact', 'in'],
        'resistance': ['exact'],
        'relapse': ['exact']
    }

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, modifier=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user)

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = PatientResource().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="patients.csv"'
        })
        return response


class BaseTestViewSet(OptimisticLockingViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'patient': ['exact', 'in'],
    }

    def perform_create(self, serializer):
        signals.set_user(self.request.user)
        serializer.save()
        signals.set_user(None)

    def perform_update(self, serializer):
        signals.set_user(self.request.user)
        serializer.save()
        signals.set_user(None)

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        resource_class = self.get_resource_class()
        dataset = resource_class().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename="{self.get_export_filename()}"'
        })
        return response

    def get_resource_class(self):
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses must implement get_resource_class()")

    def get_export_filename(self):
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses must implement get_export_filename()")


class CustomTestViewSet(BaseTestViewSet):
    queryset = CustomTest.objects.all()
    serializer_class = CustomTestSerializer
    
    def get_resource_class(self):
        return CustomTestResource

    def get_export_filename(self):
        return "customTests.csv"


class BloodTestViewSet(BaseTestViewSet):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer

    def get_resource_class(self):
        return BloodTestResource

    def get_export_filename(self):
        return "bloodTests.csv"


class LiverFunctionViewSet(BaseTestViewSet):
    queryset = LiverFunction.objects.all()
    serializer_class = LiverFunctionSerializer

    def get_resource_class(self):
        return LiverFunctionResource

    def get_export_filename(self):
        return "liverFunctions.csv"


class EchocardiographyViewSet(BaseTestViewSet):
    queryset = Echocardiography.objects.all()
    serializer_class = EchocardiographySerializer

    def get_resource_class(self):
        return EchocardiographyResource

    def get_export_filename(self):
        return "echocardiography.csv"


class InfectiousTestViewSet(BaseTestViewSet):
    queryset = InfectiousTest.objects.all()
    serializer_class = InfectiousTestSerializer

    def get_resource_class(self):
        return InfectiousTestResource

    def get_export_filename(self):
        return "others.csv"


class SamplesViewSet(BaseTestViewSet):
    queryset = Samples.objects.all()
    serializer_class = SamplesSerializer

    def get_resource_class(self):
        return SamplesResource

    def get_export_filename(self):
        return "samples.csv"


class EnrollGroupViewSet(viewsets.ModelViewSet):
    queryset = EnrollGroup.objects.all()
    serializer_class = EnrollGroupSerializer


class PatientSummaryView(APIView):
    """
    API: 返回所有病人的一般统计数据
        sample_count: 病人总数（按groups分类）
        groups：病人分组数目
        gender_counts: 性别比例（按groups分类）
        age_mean: 平均年龄（按groups分类）
    """
    @staticmethod
    def get(request):
        all_patients = Patient.objects.all()
        patient_list = [{'gender': p.gender, 'age': p.age, 'group': p.group.name} for p in all_patients]

        # 生成 dataframe
        # row_data: [[name, gender, age,...], [name, gender, age, ...], ...]
        #           => [[name, name, ...], [gender, gender, ...], ...]
        # row_data_key: ['name', 'gender', 'age', ...]
        row_data = [list(i.values()) for i in patient_list]
        row_data = np.array(row_data).transpose()
        row_data_keys = list(patient_list[0].keys())
        patient_df = pd.DataFrame(dict(zip(row_data_keys, row_data)))
        patient_df.age = patient_df.age.astype(int)

        # 提取组别数目
        groups = patient_df.group.unique()

        # 统计男女比例
        gender_count = patient_df.groupby('gender').group.value_counts().unstack().fillna(0).to_dict()

        # mean of age
        age_mean = patient_df.groupby('group').age.mean().to_dict()

        summary = {
            'sample_counts': patient_df.group.value_counts().to_dict(),
            'groups': groups,
            'gender_counts': gender_count,
            'age_mean': age_mean
        }

        return Response(summary)


class PatientCountByMonthView(APIView):
    """
    API: 返回按月统计的病人数
    """
    @staticmethod
    def get(request):
        date_count_list = [p.in_date.strftime('%Y-%m') for p in Patient.objects.order_by('in_date').all()]
        date_count_series = pd.Series(date_count_list).value_counts(sort=False)
        date_count_dict_list = [{'date': k, 'count': v} for k, v in date_count_series.items()]

        return Response(date_count_dict_list)


class PatientAgeByGroupView(APIView):
    """
    API: 返回按组分类的各患者年龄
    """
    @staticmethod
    def get(request):
        groups = EnrollGroup.objects.all()
        context = {}
        for g in groups:
            context[g.name] = [{'value': p.age / 12} for p in Patient.objects.filter(group=g).all()]
        return Response(context)


class GetAllTestsByPatientIDView(APIView):
    """
    API: 通过Patient ID 查询其所有检验数据
    """
    @staticmethod
    def get_object(pk):
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        patient = self.get_object(pk)
        blood_test = BloodTest.objects.filter(patient=patient).all()
        liver_function = LiverFunction.objects.filter(patient=patient).all()
        echocardiography = Echocardiography.objects.filter(patient=patient).all()
        infectious_test = InfectiousTest.objects.filter(patient=patient).all()
        samples = Samples.objects.filter(patient=patient).all()
        custom_tests = CustomTest.objects.filter(patient=patient).all()
        context = {
            'bloodTests': [BloodTestSerializer(bt).data for bt in blood_test],
            'liverFunction': [LiverFunctionSerializer(lf).data for lf in liver_function],
            'echocardiography': [EchocardiographySerializer(e).data for e in echocardiography],
            'infectiousTests': [InfectiousTestSerializer(ot).data for ot in infectious_test],
            'samples': [SamplesSerializer(s).data for s in samples],
            'customTests': [CustomTestSerializer(ct).data for ct in custom_tests]
        }
        for key in list(context.keys()):
            if not context.get(key):
                context.pop(key)
        return Response(context)


class ExportAllView(APIView):
    """
    API: Export All Data
    """
    @staticmethod
    def get(request):
        patients = PatientResource().export()
        blood_tests = BloodTestResource().export()
        liver_function = LiverFunctionResource().export()
        cardiography = EchocardiographyResource().export()
        infectious_test = InfectiousTestResource().export()
        custom_tests = CustomTestResource().export()
        samples = SamplesResource().export()

        with zipfile.ZipFile('/tmp/exported.zip', 'w') as zf:
            zf.writestr('patients.csv', patients.csv)
            zf.writestr('blood_test.csv', blood_tests.csv)
            zf.writestr('liver_function.csv', liver_function.csv)
            zf.writestr('cardiography.csv', cardiography.csv)
            zf.writestr('infectious_test.csv', infectious_test.csv)
            zf.writestr('custom_tests.csv', custom_tests.csv)
            zf.writestr('samples.csv', samples.csv)

        response = FileResponse(open('/tmp/exported.zip', 'rb'), as_attachment=True)

        return response
