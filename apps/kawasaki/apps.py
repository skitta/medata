from django.apps import AppConfig


class KawasakiConfig(AppConfig):
    name = 'apps.kawasaki'
    verbose_name = "Research data of Kawasaki disease"

    def ready(self):
        import apps.kawasaki.signals
