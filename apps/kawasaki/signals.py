from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import BloodTest, LiverFunction, Echocardiography, InfectiousTest, Samples, CustomTest

# This is a temporary solution to get the user from the request.
# A better solution would be to use a middleware to store the user in a thread-local variable.
# But for now, this will work.
_user = None

def set_user(user):
    global _user
    _user = user

def get_user():
    return _user

@receiver(post_save, sender=BloodTest)
@receiver(post_save, sender=LiverFunction)
@receiver(post_save, sender=Echocardiography)
@receiver(post_save, sender=InfectiousTest)
@receiver(post_save, sender=Samples)
@receiver(post_save, sender=CustomTest)
def update_patient_on_test_change(sender, instance, **kwargs):
    patient = instance.patient
    patient.modified_at = timezone.now()
    user = get_user()
    if user and user.is_authenticated:
        patient.modifier = user
    patient.save()
