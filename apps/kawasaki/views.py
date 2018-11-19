import numpy as np

from django.shortcuts import render
from django.http import HttpResponse

from scripts import zScord
from .models import Patient, Echocardiography


def index(request):
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

    # 表格表头
    headers = list(patient_list[0].keys())
    # 表格数据
    row_data = [list(i.values()) for i in patient_list]
    # 进行统计分析的表格数据
    calc_row_data = np.array([t[2:] for t in row_data])
    avg = np.average(calc_row_data, axis=0)                     # 平均值
    std = np.std(calc_row_data, axis=0)                         # 标准差
    # 统计男女比例
    gender_data = [g[1] for g in row_data]
    gender_type, gender_count = np.unique(gender_data, return_counts=True)
    gender_percent = gender_count/gender_count.sum()
    gender_summarize = np.array([gender_type, gender_count, gender_percent]).transpose()
    gender_summarize_str = []
    for i in gender_summarize:
        gender_summarize_str.append("{t}:{c}({p})".format(t=i[0], c=i[1], p=i[2]))

    context = {
        'theader': headers,
        'tbody': row_data,
        'average': np.round(avg, 2),
        'std': np.round(std, 2),
        'gender_1': gender_summarize_str[0],
        'gender_2': gender_summarize_str[1]
    }

    return render(request, 'kawasaki/index.html', context)


def update_z_score(request):
    all_echos = Echocardiography.objects.all()
    count = 0

    for echo in all_echos:
        patient = echo.patient
        echo.rca_z, echo.lmca_z = zScord.get_z_score(patient.gender, patient.height, patient.weight, echo.rca, echo.lmca)

    return HttpResponse("{n} results have updated".format(n=count))
