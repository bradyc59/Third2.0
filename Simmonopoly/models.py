from django.contrib.auth.models import AbstractUser
from django.db import models



class GamePieces(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    picture = models.FileField(upload_to='product_img', blank=True)

class CaUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
