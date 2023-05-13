from django.db import models


# Create your models here.
class Chat(models.Model):
    Title = models.CharField(max_length=50)
    File = models.FileField(upload_to="utils/files")
