from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.

class tasklist(models.Model):

    manage = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)
    priority = models.IntegerField(null=True, blank=True)
    start_on = models.DateField(null=True, blank=True)
    start_at = models.TimeField(null=True, blank=True)
    end_on = models.DateField(null=True, blank=True)
    end_at = models.TimeField(null=True, blank=True)
    point = models.IntegerField(null=True, blank=True,default=0)

    def __str__(self):
        return '{} {} {} {}'.format(self.task, self.start_on, self.point)
 