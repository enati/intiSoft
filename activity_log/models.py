from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType


class ActivityLog(models.Model):
    datetime = models.DateTimeField("Fecha")
    activity = models.CharField("Actividad", max_length=500)
    comments = models.CharField("Observaciones", max_length=800)
    content_type = models.ForeignKey(ContentType, verbose_name="Modelo")
    object_id = models.PositiveIntegerField()

    def __str__(self):
        return "%s - %s" % (self.datetime.__format__("%d/%m/%y %H:%M"), self.activity)

    class Meta:
        ordering = ['-datetime']
