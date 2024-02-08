import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class AdvUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')

    class Meta(AbstractUser.Meta):
        pass
