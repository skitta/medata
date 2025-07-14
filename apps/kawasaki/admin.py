from django.contrib import admin

from .models import Patient, BloodTest, LiverFunction, Echocardiography, InfectiousTest, EnrollGroup, Samples, CustomTest


admin.site.site_title = 'Medata'
admin.site.site_header = 'Patients Medical Data System'


class BloodTestInline(admin.TabularInline):
    model = BloodTest
    extra = 1


class LiverFunctionInline(admin.TabularInline):
    model = LiverFunction
    extra = 1


class EchocardiographyInline(admin.TabularInline):
    model = Echocardiography
    extra = 1


class InfectiousTestInline(admin.TabularInline):
    model = InfectiousTest
    extra = 1


class CustomTestInline(admin.TabularInline):
    model = CustomTest
    extra = 1


class SamplesInline(admin.TabularInline):
    model = Samples
    extra = 1


@admin.register(EnrollGroup)
class EnrollGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('registered_ID', 'full_name', 'in_date', 'group', 'resistance', 'relapse')
    inlines = [BloodTestInline, LiverFunctionInline, EchocardiographyInline, InfectiousTestInline, CustomTestInline, SamplesInline]


@admin.register(BloodTest)
class BloodTestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'wbc', 'plt')


@admin.register(LiverFunction)
class LiverFunctionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'ast', 'alt', 'tb', 'alb')


@admin.register(Echocardiography)
class EchocardiographyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'lmca', 'lmca_z', 'rca', 'rca_z')


@admin.register(InfectiousTest)
class infectiousTestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'pct', 'crp')


@admin.register(CustomTest)
class CustomTestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'name', 'result', 'notes')


@admin.register(Samples)
class SamplesAdmin(admin.ModelAdmin):
    list_display = ('patient', 'label', 'date', 'sample_type', 'sample_status')
