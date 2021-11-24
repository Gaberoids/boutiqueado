# This will be used to tell the engine to grab the static files and images from amazon when depoying the site
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# new class inheriting S3botoStorage
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
