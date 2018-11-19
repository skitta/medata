from django.db import models


class Patient(models.Model):
    registered_ID = models.CharField(max_length=8, unique=True)
    document_ID = models.CharField(max_length=7, null=True)
    full_name = models.CharField(max_length=20)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    in_date = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    
    def __str__(self):
        return "{name}({id})".format(name=self.full_name, id=self.registered_ID)


class BloodTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    wbc = models.FloatField()
    ne = models.FloatField()
    ly = models.FloatField()
    mo = models.FloatField()
    rbc = models.FloatField()
    plt = models.FloatField()

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)


class LiverFunction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    ast = models.IntegerField(null=True)
    alt = models.IntegerField(null=True)
    pa = models.IntegerField(null=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)


class Echocardiography(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    lmca = models.FloatField()
    lmca_z = models.FloatField(null=True, editable=False)
    rca = models.FloatField()
    rca_z = models.FloatField(null=True, editable=False)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)


class OtherTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    pct = models.FloatField(null=True)
    crp = models.FloatField(null=True)
    mp_igm = models.FloatField(null=True)

    def __str__(self):
        return "{patient}({date})".format(patient=self.patient.full_name, date=self.date)

