# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0026_auto_20150925_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec',
            name='tipo_servicio',
            field=models.CharField(max_length=20, verbose_name=b'Tipo de Servicio', choices=[(b'', b'ASIST. TECNICA'), (b'', b'DESARROLLO'), (b'', b'CAPACITACION'), (b'', b'LOGISTICA'), (b'', b'ENSAYOS'), (b'', b'AUDITORIA'), (b'', b'CALIBRACION'), (b'', b'CERT. OBLIGATORIA')]),
        ),
    ]
