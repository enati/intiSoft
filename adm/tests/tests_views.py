from django.test import TestCase
from django.test import Client
from django.utils import timezone
import datetime
from adm.views import *
from adm.models import Presupuesto, Usuario, OfertaTec
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, Group, User
from django.test.utils import setup_test_environment


#========================================================
#================= FUNCIONES AUXILIARES =================
#========================================================


def create_admin_group():
    group = Group.objects.create(name='Administracion')
    for p in Permission.objects.filter(content_type__app_label__in=['adm']):
        group.permissions.add(p)
    return group


def create_lab_group(lab):
    group = Group.objects.create(name=lab)
    for p in Permission.objects.filter(content_type__app_label=lab):
        group.permissions.add(p)
    return group


def create_user(name, pwd, mail, group):
    user = User.objects.create_user(name, mail, pwd)
    user.groups.add(group)
    return user


class PresupuestoFormTest(TestCase):
    labs = ['LIM1', 'LIM2', 'LIM3', 'LIM4', 'LIM5', 'LIM6', 'LIA', 'EXT', 'SIS', 'CAL', 'MEC', 'ML']
    fixtures = ['users.json']
    requiredFormsetFields = { 'instrumento_set-0-id': [''],
                              'instrumento_set-TOTAL_FORMS': ['1'],
                              'instrumento_set-0-fecha_llegada': [''],
                              'instrumento_set-MAX_NUM_FORMS': ['1000'],
                              'instrumento_set-0-nro_recepcion': [''],
                              'instrumento_set-INITIAL_FORMS': ['0'],
                              'instrumento_set-MIN_NUM_FORMS': ['1']
                            }

    #@classmethod
    #def setUpTestData(cls):
        ## Creo un usuario correspondiente a cada area
        #cls.users = {}
        #adminGroup = create_admin_group()
        #cls.users['admin'] = create_user('admin', 'admin', '', adminGroup)
        #for lab in cls.labs:
            #labGroup = create_lab_group(lab)
            #cls.users[lab] = create_user(lab, lab, '', labGroup)

    #def setUp(self):
        ## Creo un usuario
        #self.user = Usuario(nro_usuario='0001',
                            #nombre='Juan',
                            #cuit='30349342406',
                            #rubro='Autopartista')

    #def setUp_env(self, group):
        #"""
        #Me logueo al cliente con un usuario del grupo 'group'
        #"""
        #user = self.users[group]
        #loginOk = self.client.login(username=user.username,
                          #password=user.natural_key()[0])
        #self.assertTrue(loginOk, "Error en el login")

    #def test_passed_to_aceptado_in_create(self):
        #"""
        #El presupuesto debe pasar a estado aceptado cuando se crea con
        #fecha de aceptacion.
        #"""
        #self.setUp_env('admin')

        #usuario = Usuario.objects.all()[0]
        ##Creo un presupuesto con fecha de aceptacion desde el formulario web
        #vals = {
            #'codigo': '00001',
            #'fecha_solicitado': (timezone.now() -
                              #datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            #'fecha_realizado': (timezone.now() -
                             #datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            #'fecha_aceptado': (timezone.now() -
                            #datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
            #'usuario': usuario.id,
            #'estado': 'borrador',
        #}
        #vals.update(self.requiredFormsetFields)

        #response = self.client.post(reverse('adm:presup-create'), vals, follow=True)

        ## Luego del create se tiene que mostrar el template del update
        #self.assertEqual(response.resolver_match.func.__name__, PresupuestoUpdate.as_view().__name__)
        #self.assertEqual(response.status_code, 200)
        #presup = Presupuesto.objects.get(codigo='00001')
        #self.assertEqual(presup.estado, 'aceptado')

    #def test_init_state_borrador(self):
        #"""
        #El presupuesto debe estar en estado borrador cuando se crea sin
        #fecha de aceptacion.
        #"""
        #self.setUp_env('admin')

        #usuario = Usuario.objects.all()[0]

        ##Creo un presupuesto sin fecha de aceptacion desde el formulario web
        #vals = {
            #'codigo': '0002',
            #'fecha_solicitado': (timezone.now() -
                              #datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            #'fecha_realizado': (timezone.now() -
                             #datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            #'usuario': usuario.id,
            #'estado': 'borrador',
        #}
        #response = self.client.post(reverse('adm:presup-create'), vals)
        #self.assertEqual(response.status_code, 302)
        #presup = Presupuesto.objects.get(codigo='0002')
        #self.assertEqual(presup.estado, 'borrador')

    #def test_perm_required_create(self):
        #"""
        #Solo los usuarios logueados y  con permisos de creacion en presupuestos
        #pueden crear presupuestos.
        #"""
        ## Sin login (redirecciona a la pagina de login, por eso el 302)
        #response = self.client.get(reverse('adm:presup-create'))
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        #response = self.client.post(reverse('adm:presup-create'), {})
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        ## Sin permisos (para cualquier laboratorio)
        #for lab in self.labs:
            #self.setUp_env(lab)
            #response = self.client.get(reverse('adm:presup-create'))
            #self.assertEqual(response.status_code, 403)
            #response = self.client.post(reverse('adm:presup-create'), {})
            #self.assertEqual(response.status_code, 403)
            #self.client.logout()

    #def test_perm_required_update(self):
        #"""
        #Solo los usuarios logueados y  con permisos de modificacion en
        #presupuestos pueden modificar presupuestos.
        #"""
        ## Sin login (redirecciona a la pagina de login, por eso el 302)
        #response = self.client.get(reverse('adm:presup-update',
                                           #kwargs={'pk': '1'}))
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        #response = self.client.post(reverse('adm:presup-update',
                                            #kwargs={'pk': '1'}), {})
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        ## Sin permisos (para cualquier laboratorio)
        #for lab in self.labs:
            #self.setUp_env(lab)
            #response = self.client.get(reverse('adm:presup-update',
                                               #kwargs={'pk': '1'}))
            #self.assertEqual(response.status_code, 403)
            #response = self.client.post(reverse('adm:presup-update',
                                                #kwargs={'pk': '1'}), {})
            #self.assertEqual(response.status_code, 403)
            #self.client.logout()

    #def test_perm_required_delete(self):
        #"""
        #Solo los usuarios logueados y  con permisos de eliminacion en
        #presupuestos pueden eliminar presupuestos.
        #"""
        ## Sin login (redirecciona a la pagina de login, por eso el 302)
        #response = self.client.get(reverse('adm:presup-list'))
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        #response = self.client.post(reverse('adm:presup-list'),
                                            #{'Eliminar': '1'})
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        ## Sin permisos (para cualquier laboratorio)
        #for lab in self.labs:
            #self.setUp_env(lab)
            #response = self.client.post(reverse('adm:presup-list'),
                                                #{'Eliminar': '1'})
            #self.assertEqual(response.status_code, 403)
            #self.client.logout()

    #def test_perm_required_finish(self):
        #"""
        #Solo los usuarios logueados y  con permisos de finalizacion en
        #presupuestos pueden finalizar presupuestos.
        #"""
        ## Sin login (redirecciona a la pagina de login, por eso el 302)
        #response = self.client.get(reverse('adm:presup-list'))
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        #response = self.client.post(reverse('adm:presup-list'),
                                            #{'Finalizar': '1'})
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        ## Sin permisos (para cualquier laboratorio)
        #for lab in self.labs:
            #self.setUp_env(lab)
            #response = self.client.post(reverse('adm:presup-list'),
                                                #{'Finalizar': '1'})
            #self.assertEqual(response.status_code, 403)
            #self.client.logout()

    #def test_perm_required_cancel(self):
        #"""
        #Solo los usuarios logueados y  con permisos de cancelacion en
        #presupuestos pueden cancelar presupuestos.
        #"""
        ## Sin login (redirecciona a la pagina de login, por eso el 302)
        #response = self.client.get(reverse('adm:presup-list'))
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        #response = self.client.post(reverse('adm:presup-list'),
                                            #{'Cancelar': '1'})
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.content, '')
        ## Sin permisos (para cualquier laboratorio)
        #for lab in self.labs:
            #self.setUp_env(lab)
            #response = self.client.post(reverse('adm:presup-list'),
                                                #{'Cancelar': '1'})
            #self.assertEqual(response.status_code, 403)
            #self.client.logout()
