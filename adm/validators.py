# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator, EmailValidator

alphabetic = RegexValidator(r'^([A-Za-z]|[áéíóú]|[ \'])*$', 'Solo se permiten caracteres alfabéticos.')