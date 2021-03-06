from django.contrib import admin

from .models import Patient, BloodTest, LiverFunction, Echocardiography, OtherTest


class BloodTestInline(admin.TabularInline):
    model = BloodTest
    extra = 1


class LiverFunctionInline(admin.TabularInline):
    model = LiverFunction
    extra = 1


class EchocardiographyInline(admin.TabularInline):
    model = Echocardiography
    extra = 1


class OtherTestInline(admin.TabularInline):
    model = OtherTest
    extra = 1


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('registered_ID', 'full_name', 'in_date')
    inlines = [BloodTestInline, LiverFunctionInline, EchocardiographyInline, OtherTestInline]


@admin.register(BloodTest)
class BloodTestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'wbc', 'plt')


@admin.register(LiverFunction)
class LiverFunctionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'ast', 'alt', 'pa')


@admin.register(Echocardiography)
class EchocardiographyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'lmca', 'lmca_z', 'rca', 'rca_z')


@admin.register(OtherTest)
class OtherTestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'pct', 'crp', 'mp_igm')
