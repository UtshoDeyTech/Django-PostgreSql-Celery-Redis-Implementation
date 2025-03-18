from django.apps import AppConfig


class CeleryWorkerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_worker_app'
