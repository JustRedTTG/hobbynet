import atexit
import tempfile

from django.conf import settings

settings.DEBUG = True
settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
settings.INSTALLED_APPS.remove('django_backblaze_b2')
del settings.CACHES['django-backblaze-b2']

media_temp_dir = tempfile.TemporaryDirectory()
settings.MEDIA_ROOT = media_temp_dir.name
settings.MEDIA_URL = '/media/'