from django.apps import AppConfig


class DemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'milea_demo'
    verbose_name = "Demo"
    menu_icon = "ti ti-building-factory-2"
    menu_firstlvl = ['DefaultModal',]
    menu_secondlvl = [("Konfiguration", ['Tag'])]
