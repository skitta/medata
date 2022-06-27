from django.db import models


class EnrollGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name='组名称')

    def __str__(self):
        return "{}".format(self.name)

    class Meta(object):
        verbose_name = '分组'
        verbose_name_plural = verbose_name


class Patient(models.Model):
    registered_ID = models.CharField(max_length=10, unique=True, verbose_name='登记号')
    document_ID = models.CharField(max_length=10, null=True, verbose_name='住院号')
    full_name = models.CharField(max_length=20, verbose_name='姓名')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄（月）')
    in_date = models.DateField(verbose_name='入院日期')
    weight = models.FloatField(verbose_name='体重（Kg）')
    height = models.FloatField(verbose_name='身高（cm）')
    group = models.ForeignKey(EnrollGroup, on_delete=models.CASCADE, verbose_name='分组')
    resistance = models.BooleanField(verbose_name='IVIG 抵抗', default=False)
    relapse = models.BooleanField(verbose_name='复发', default=False)
    
    def __str__(self):
        return "{name}({id})".format(name=self.full_name, id=self.registered_ID)

    class Meta(object):
        verbose_name = '病人'
        verbose_name_plural = verbose_name


class BloodTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    date = models.DateField(verbose_name='检验日期')
    wbc = models.FloatField(verbose_name='白细胞计数')
    ne = models.FloatField(verbose_name='中性粒占比（%）')
    ly = models.FloatField(verbose_name='淋巴占比（%）')
    mo = models.FloatField(verbose_name='单核占比（%）')
    rbc = models.FloatField(verbose_name='红细胞计数')
    plt = models.FloatField(verbose_name='血小板计数')

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

    class Meta(object):
        verbose_name = '血常规'
        verbose_name_plural = verbose_name


class LiverFunction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    date = models.DateField(verbose_name='检验日期')
    ast = models.IntegerField(null=True, verbose_name='AST', blank=True)
    alt = models.IntegerField(null=True, verbose_name='ALT', blank=True)
    pa = models.IntegerField(null=True, verbose_name='前白蛋白', blank=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

    class Meta(object):
        verbose_name = '肝功能'
        verbose_name_plural = verbose_name


class Echocardiography(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    date = models.DateField(verbose_name='检验日期')
    lmca = models.FloatField(verbose_name='左主干')
    lmca_z = models.FloatField(null=True, verbose_name='左主干Z值', blank=True)
    rca = models.FloatField(verbose_name='右支')
    rca_z = models.FloatField(null=True, verbose_name='右支Z值', blank=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

    class Meta(object):
        verbose_name = '心脏彩超'
        verbose_name_plural = verbose_name


class OtherTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    date = models.DateField(verbose_name='检验日期')
    pct = models.FloatField(null=True, verbose_name='降钙素原', blank=True)
    crp = models.FloatField(null=True, verbose_name='超敏C反应蛋白', blank=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

    class Meta(object):
        verbose_name = '其他辅助检查'
        verbose_name_plural = verbose_name


class Samples(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    label = models.CharField(max_length=10, verbose_name='标签', unique=True)
    date = models.DateField(verbose_name='收集日期')

    TYPE_CHOICES = (
        ('0', '全血'),
        ('1', '血清'),
        ('2', '血浆'),
        ('3', 'PBMCs'),
        ('4', '其他组织'),
    )
    sample_type = models.CharField(max_length=1, choices=TYPE_CHOICES, verbose_name='标本类型')

    STATUS_CHOICES = (
        ('0', '待处理'),
        ('1', '已处理'),
        ('2', '已销毁'),
    )
    sample_status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='标本状态')

    note = models.TextField(null=True, verbose_name='备注', blank=True)

    def __str__(self):
        return '{}({})'.format(self.label, self.patient.full_name)

    class Meta(object):
        verbose_name = '标本'
        verbose_name_plural = verbose_name
