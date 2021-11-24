from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# The code below is saying that anytime I git push, on the deployment, all the static files from github or gitpod, should go to AWS
# new class inheriting S3botoStorage
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

# the code below is saying in production  anytime someone is uploading a product image, to store it in the AWS
class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
