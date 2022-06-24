import numpy as np
import pandas as pd

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

# from scripts import zScord

from .models import Patient, Echocardiography, BloodTest, LiverFunction, EnrollGroup, OtherTest, Samples
from .serializers import PatientSerializer, BloodTestSerializer, LiverFunctionSerializer, EchocardiographySerializer, EnrollGroupSerializer, OtherTestSerializer, SamplesSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('id')
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=registered_ID']


class BloodTestViewSet(viewsets.ModelViewSet):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer


class LiverFunctionViewSet(viewsets.ModelViewSet):
    queryset = LiverFunction.objects.all()
    serializer_class = LiverFunctionSerializer


class EchocardiographyViewSet(viewsets.ModelViewSet):
    queryset = Echocardiography.objects.all()
    serializer_class = EchocardiographySerializer


class OtherTestViewSet(viewsets.ModelViewSet):
    queryset = OtherTest.objects.all()
    serializer_class = OtherTestSerializer


class SamplesViewSet(viewsets.ModelViewSet):
    queryset = Samples.objects.all()
    serializer_class = SamplesSerializer


class EnrollGroupViewSet(viewsets.ModelViewSet):
    queryset = EnrollGroup.objects.all()
    serializer_class = EnrollGroupSerializer


class PatientSummaryView(APIView):
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


# !!! do not delete
# def update_z_score(request):
#     all_echos = Echocardiography.objects.all()
#     count = 0
#
#     for echo in all_echos:
#         patient = echo.patient
#         echo.rca_z, echo.lmca_z = zScord.get_z_score(patient.gender, patient.height, patient.weight, echo.rca, echo.lmca)
#
#     return Response({'msg': "{n} results have updated".format(n=count)})


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
    API: 返回患者的年龄信息
    """
    @staticmethod
    def get(request):
        groups = EnrollGroup.objects.all()
        context = {}
        for g in groups:
            context[g.name] = [{'value': p.age / 12} for p in Patient.objects.filter(group=g).all()]
        return Response(context)
