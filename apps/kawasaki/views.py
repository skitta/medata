import numpy as np

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from scripts import zScord

from .models import Patient, Echocardiography, BloodTest, LiverFunction
from .serializers import PatientSerializer, BloodTestSerializer, LiverFunctionSerializer, EchocardiographySerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class BloodTestViewSet(viewsets.ModelViewSet):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer
    permission_classes = [permissions.IsAuthenticated]


class LiverFunctionViewSet(viewsets.ModelViewSet):
    queryset = LiverFunction.objects.all()
    serializer_class = LiverFunctionSerializer
    permission_classes = [permissions.IsAuthenticated]


class EchocardiographyViewSet(viewsets.ModelViewSet):
    queryset = Echocardiography.objects.all()
    serializer_class = EchocardiographySerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientSummaryView(APIView):
    def get(self, request):
        patient_list = []
        all_patients = Patient.objects.all()
        for p in all_patients:
            item = {'name': p.full_name, 'gender': p.gender, 'age': p.age, 'height': p.height}

            # 首次血常规
            first_bt = p.bloodtest_set.order_by('date').first()
            item['wbc'] = first_bt.wbc
            item['plt'] = first_bt.plt

            # 血小板计数最高时刻的血常规
            max_plt_bt = p.bloodtest_set.order_by('-plt').first()
            item['plt_max'] = max_plt_bt.plt

            # 首次其他血清检查
            first_ot = p.othertest_set.order_by('date').first()
            item['pct'] = first_ot.pct or 0
            item['crp'] = first_ot.crp or 0

            # 任意冠脉Z值最大时刻的超声心动图检查
            max_rca_z_echo = p.echocardiography_set.order_by('-rca_z').first()
            max_lmca_z_echo = p.echocardiography_set.order_by('-lmca_z').first()
            if max_rca_z_echo.rca_z > max_lmca_z_echo.lmca_z:
                item['rca_z'] = max_rca_z_echo.rca_z
                item['lmca_z'] = max_rca_z_echo.lmca_z
            else:
                item['rca_z'] = max_lmca_z_echo.rca_z
                item['lmca_z'] = max_lmca_z_echo.lmca_z

            patient_list.append(item)

        # 表格数据
        row_data = [list(i.values()) for i in patient_list]
        # 进行统计分析的表格数据
        calc_row_data = np.array([t[2:] for t in row_data])
        row_data_keys = list(patient_list[0].keys())[2:]
        avg = np.average(calc_row_data, axis=0)                     # 平均值
        std = np.std(calc_row_data, axis=0)                         # 标准差
        # 统计男女比例
        gender_data = [g[1] for g in row_data]
        gender_type, gender_count = np.unique(gender_data, return_counts=True)
        gender_percent = gender_count/gender_count.sum()
        gender_summarize = np.array([gender_type, gender_count, gender_percent]).transpose()

        statistics = {
            'average': dict(zip(row_data_keys, avg)),
            'std': dict(zip(row_data_keys, std)),
            'gender_summarize': [dict(zip(['type', 'count', 'percent'], i)) for i in gender_summarize]
        }

        context = {
            'patient_list': patient_list,
            'statistics': statistics
        }

        return Response(context)


def update_z_score(request):
    all_echos = Echocardiography.objects.all()
    count = 0

    for echo in all_echos:
        patient = echo.patient
        echo.rca_z, echo.lmca_z = zScord.get_z_score(patient.gender, patient.height, patient.weight, echo.rca, echo.lmca)

    return Response({'msg': "{n} results have updated".format(n=count)})
