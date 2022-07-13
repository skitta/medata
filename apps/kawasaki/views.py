import numpy as np
import pandas as pd
import zipfile

from django.http import Http404, HttpResponse, FileResponse

from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from .models import Patient, Echocardiography, BloodTest, LiverFunction, EnrollGroup, OtherTest, Samples
from .serializers import PatientSerializer, BloodTestSerializer, LiverFunctionSerializer, EchocardiographySerializer,\
    EnrollGroupSerializer, OtherTestSerializer, SamplesSerializer
from .resource import PatientResource, BloodTestResource, LiverFunctionResource, EchocardiographyResource, \
    OtherTestResource, SamplesResource


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('id')
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['=registered_ID', 'full_name']
    filterset_fields = {
        'group': ['exact', 'in'],
        'resistance': ['exact'],
        'relapse': ['exact']
    }

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = PatientResource().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="patients.csv"'
        })
        return response


class BloodTestViewSet(viewsets.ModelViewSet):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'patient': ['exact', 'in'],
    }

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = BloodTestResource().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="bloodTests.csv"'
        })
        return response


class LiverFunctionViewSet(viewsets.ModelViewSet):
    queryset = LiverFunction.objects.all()
    serializer_class = LiverFunctionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'patient': ['exact', 'in'],
    }

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = LiverFunctionResource().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="liverFunctions.csv"'
        })
        return response


class EchocardiographyViewSet(viewsets.ModelViewSet):
    queryset = Echocardiography.objects.all()
    serializer_class = EchocardiographySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'patient': ['exact', 'in'],
    }

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = EchocardiographyResource().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="echocardiography.csv"'
        })
        return response


class OtherTestViewSet(viewsets.ModelViewSet):
    queryset = OtherTest.objects.all()
    serializer_class = OtherTestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'patient': ['exact', 'in'],
    }

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = OtherTestResource().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="others.csv"'
        })
        return response


class SamplesViewSet(viewsets.ModelViewSet):
    queryset = Samples.objects.all()
    serializer_class = SamplesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'patient': ['exact', 'in'],
    }

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = SamplesResource().export(queryset)
        response = HttpResponse(dataset.csv, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="samples.csv"'
        })
        return response


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
        other_test = OtherTest.objects.filter(patient=patient).all()
        samples = Samples.objects.filter(patient=patient).all()
        context = {
            'bloodTests': [BloodTestSerializer(bt).data for bt in blood_test],
            'liverFunction': [LiverFunctionSerializer(lf).data for lf in liver_function],
            'echocardiography': [EchocardiographySerializer(e).data for e in echocardiography],
            'otherTests': [OtherTestSerializer(ot).data for ot in other_test],
            'samples': [SamplesSerializer(s).data for s in samples]
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
        other_tests = OtherTestResource().export()
        samples = SamplesResource().export()

        with zipfile.ZipFile('/tmp/exported.zip', 'w') as zf:
            zf.writestr('patients.csv', patients.csv)
            zf.writestr('blood_test.csv', blood_tests.csv)
            zf.writestr('liver_function.csv', liver_function.csv)
            zf.writestr('cardiography.csv', cardiography.csv)
            zf.writestr('other_test.csv', other_tests.csv)
            zf.writestr('samples.csv', samples.csv)

        response = FileResponse(open('/tmp/exported.zip', 'rb'), as_attachment=True)

        return response
