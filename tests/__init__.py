from django.conf import settings


settings.DEBUG = True
settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
settings.INSTALLED_APPS.remove('django_backblaze_b2')
del settings.CACHES['django-backblaze-b2']

settings.MEDIA_ROOT = settings.BASE_DIR / 'media'
settings.MEDIA_URL = '/media/'