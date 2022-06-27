from django.contrib import admin

from .models import Patient, BloodTest, LiverFunction, Echocardiography, OtherTest, EnrollGroup, Samples


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


class OtherTestInline(admin.TabularInline):
    model = OtherTest
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
    inlines = [BloodTestInline, LiverFunctionInline, EchocardiographyInline, OtherTestInline, SamplesInline]


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
    list_display = ('patient', 'date', 'pct', 'crp')


@admin.register(Samples)
class SamplesAdmin(admin.ModelAdmin):
    list_display = ('patient', 'label', 'date', 'sample_type', 'sample_status')
