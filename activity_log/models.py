from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from audit_log.models import AuthStampedModel


class ActivityLog(AuthStampedModel):
    datetime = models.DateTimeField("Fecha")
    activity = models.CharField("Actividad", max_length=500)
    comments = models.CharField("Observaciones", max_length=800)
    content_type = models.ForeignKey(ContentType, verbose_name="Modelo")
    object_id = models.PositiveIntegerField()

    def __str__(self):
        return "%s - %s" % (self.datetime.__format__("%d/%m/%y %H:%M"), self.activity)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.datetime = datetime.now()
        super(ActivityLog, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-datetime']
