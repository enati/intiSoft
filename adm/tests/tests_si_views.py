# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.utils import timezone
import datetime
from adm.views import *
from adm.models import Presupuesto, Usuario, OfertaTec
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, Group, User
from django.test.utils import setup_test_environment
from adm.tests.utils import *


#class SICreateTest(TestCase):
    #labs = ['LIM1', 'LIM2', 'LIM3', 'LIM4', 'LIM5', 'LIM6', 'LIA', 'EXT', 'SIS', 'CAL', 'MEC', 'ML']

    #requiredFormsetFields = {
                             #'id_adm-ot_linea-content_type-object_id-TOTAL_FORMS': ['1'],
                             #'id_adm-ot_linea-content_type-object_id-MAX_NUM_FORMS': ['1000'],
                             #'id_adm-ot_linea-content_type-object_id-INITIAL_FORMS': ['0'],
                             #'id_adm-ot_linea-content_type-object_id-MIN_NUM_FORMS': ['1'],
                             #'id_adm-tarea_linea-content_type-object_id-TOTAL_FORMS': ['1'],
                             #'id_adm-tarea_linea-content_type-object_id-MAX_NUM_FORMS': ['1000'],
                             #'id_adm-tarea_linea-content_type-object_id-INITIAL_FORMS': ['0'],
                             #'id_adm-tarea_linea-content_type-object_id-MIN_NUM_FORMS': ['1'],
                            #}

    #@classmethod
    #def setUpTestData(cls):
        ## Creo un usuario correspondiente a cada area
        #cls.users = {}
        #siGroup = create_si_group()
        #adminGroup = create_admin_group()
        #cls.users['admin'] = create_user('admin', 'admin', '', adminGroup)
        #for lab in cls.labs:
            #labGroup = create_lab_group(lab)
            #user = create_user(lab, lab, '', labGroup)
            #user.groups.add(siGroup)
            #cls.users[lab] = user

    #def setUp(self):
        #pass

    #def setUp_env(self, group):
        #"""
        #Me logueo al cliente con un usuario del grupo 'group'
        #"""
        #user = self.users[group]
        #loginOk = self.client.login(username=user.username,
                          #password=user.natural_key()[0])
        #self.assertTrue(loginOk, "Error en el login")

    #def test_user_limit_ut_ejecutora_in_create(self):
        #"""
        #El usuario solo debe poder elegir como area ejecutora un area a la cual pertenezca
        #"""

        #self.setUp_env('LIA')

        #vals = { 'codigo': '00001',
                 #'fecha_prevista': datetime.now(),
                 #'solicitante': 'LIA',
                 #'ejecutor': 'DES'
            #}
        #import pdb; pdb.set_trace()
        #response = self.client.post(reverse('adm:si-create'), vals, follow=True)
        #self.assertEqual(response.resolver_match.func.__name__, SICreate.as_view().__name__)