from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


class OptimisticLockingModel(models.Model):
    version = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # This is a new object, so we can just save it.
            super().save(*args, **kwargs)
        else:
            # This is an existing object, so we need to check the version atomically.
            # Use update() with a WHERE clause to ensure atomicity
            current_version = self.version
            updated_rows = self.__class__.objects.filter(
                pk=self.pk, 
                version=current_version
            ).update(version=F('version') + 1)
            
            if updated_rows == 0:
                # No rows were updated, meaning the version has changed
                raise ValidationError('Stale data detected. Please reload and try again.')
            
            # Update the version field in memory to match database
            self.version = current_version + 1
            
            # Now save the rest of the fields with update_fields to avoid version conflicts
            update_fields = kwargs.pop('update_fields', None)
            if update_fields is None:
                # Get all field names except version (already updated)
                update_fields = [f.name for f in self._meta.fields if f.name != 'version' and f.name != 'id']
            
            # Use update() for atomic field updates
            field_updates = {field: getattr(self, field) for field in update_fields}
            self.__class__.objects.filter(pk=self.pk).update(**field_updates)


class EnrollGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name='组名称')

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = '分组'
        verbose_name_plural = verbose_name


class Patient(OptimisticLockingModel):
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
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_patients', verbose_name='创建者')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_patients', verbose_name='修改者')
    
    def __str__(self):
        return "{name}({id})".format(name=self.full_name, id=self.registered_ID)

    @property
    def creator_full_name(self):
        if self.creator:
            return f"{self.creator.first_name}{self.creator.last_name}".strip()
        return "N/A"
    
    @property
    def modifier_full_name(self):
        if self.modifier:
            return f"{self.modifier.first_name}{self.modifier.last_name}".strip()
        return "N/A"

    class Meta(OptimisticLockingModel.Meta):
        verbose_name = '病人'
        verbose_name_plural = verbose_name


class BloodTest(OptimisticLockingModel):
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

    class Meta(OptimisticLockingModel.Meta):
        verbose_name = '血常规'
        verbose_name_plural = verbose_name


class LiverFunction(OptimisticLockingModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    date = models.DateField(verbose_name='检验日期')
    ast = models.IntegerField(null=True, verbose_name='AST', blank=True)
    alt = models.IntegerField(null=True, verbose_name='ALT', blank=True)
    
    tbil = models.FloatField(null=True, verbose_name='总胆红素', blank=True)
    dbil = models.FloatField(null=True, verbose_name='直接胆红素', blank=True)
    tb = models.FloatField(null=True, verbose_name='总蛋白', blank=True)
    alb = models.FloatField(null=True, verbose_name='白蛋白', blank=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

    class Meta(OptimisticLockingModel.Meta):
        verbose_name = '肝功能'
        verbose_name_plural = verbose_name


class Echocardiography(OptimisticLockingModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    date = models.DateField(verbose_name='检验日期')
    lmca = models.FloatField(verbose_name='左主干')
    lmca_z = models.FloatField(null=True, verbose_name='左主干Z值', blank=True)
    rca = models.FloatField(verbose_name='右支')
    rca_z = models.FloatField(null=True, verbose_name='右支Z值', blank=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

    class Meta(OptimisticLockingModel.Meta):
        verbose_name = '心脏彩超'
        verbose_name_plural = verbose_name


class InfectiousTest(OptimisticLockingModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    date = models.DateField(verbose_name='检验日期')
    pct = models.FloatField(null=True, verbose_name='降钙素原', blank=True)
    crp = models.FloatField(null=True, verbose_name='超敏C反应蛋白', blank=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

    class Meta(OptimisticLockingModel.Meta):
        verbose_name = '感染性指标'
        verbose_name_plural = verbose_name


class Samples(OptimisticLockingModel):
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

    class Meta(OptimisticLockingModel.Meta):
        verbose_name = '标本'
        verbose_name_plural = verbose_name


class CustomTest(OptimisticLockingModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='病人')
    name = models.CharField(max_length=100, verbose_name='检验名称')
    date = models.DateField(verbose_name='检验日期')
    result = models.FloatField(verbose_name='检验结果')
    notes = models.TextField(blank=True, verbose_name='备注')

    def __str__(self):
        return f"{self.patient.full_name} - {self.name} ({self.date})"

    class Meta(OptimisticLockingModel.Meta):
        verbose_name = '其他辅助检查'
        verbose_name_plural = verbose_name
