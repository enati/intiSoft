from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Presupuesto, Usuario, OfertaTec
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, Group, User
from django.test.utils import setup_test_environment


def get_or_create_admin_group():
    group, created = Group.objects.get_or_create(name='Administracion')
    for p in Permission.objects.filter(content_type__app_label__in=
                                                              ['adm', 'lab']):
        group.permissions.add(p)
    return group


def get_or_create_lab_group():
    group, created = Group.objects.get_or_create(name='Laboratorista')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        group.permissions.add(p)
    return group


def create_adm_user():
    user = User.objects.create_user('admin',
                                    'admin@gmail.com',
                                    'admin')
    adm_group = get_or_create_admin_group()
    user.groups.add(adm_group)
    return user


def create_lab_user():
    user = User.objects.create_user('lab',
                                    'lab@gmail.com',
                                    'lab')
    lab_group = get_or_create_lab_group()
    user.groups.add(lab_group)
    return user


class PresupuestoTest(TestCase):

    def setUp_adm_env(self):
        # Busco/creo un usuario del grupo 'Administracion'
        try:
            user = User.objects.get(username='admin')
        except:
            user = create_adm_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_lab_env(self):
        # Busco/creo un usuario del grupo 'Laboratorista'
        try:
            user = User.objects.get(username='lab')
        except:
            user = create_lab_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def test_passed_to_aceptado_in_create(self):
        """
        El presupuesto debe pasar a estado aceptado cuando se crea con
        fecha de aceptacion.
        """
        self.setUp_adm_env()

        usuario = Usuario(nro_usuario='0001',
                          nombre='Juan',
                          cuit='30349342406',
                          rubro='Autopartista')
        usuario.save()

        #Creo un presupuesto con fecha de aceptacion desde el formulario web
        vals = {
            'codigo': '0001',
            'fecha_solicitado': (timezone.now() -
                              datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_realizado': (timezone.now() -
                             datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_aceptado': (timezone.now() -
                            datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
            'usuario': usuario.id,
            'estado': 'borrador',
        }
        response = self.client.post(reverse('adm:presup-create'), vals)
        self.assertEqual(response.status_code, 200)
        presup = Presupuesto.objects.get(codigo='0001')
        self.assertEqual(presup.estado, 'aceptado')

    def test_init_state_borrador(self):
        """
        El presupuesto debe estar en estado borrador cuando se crea sin
        fecha de aceptacion.
        """
        self.setUp_adm_env()

        usuario = Usuario(nro_usuario='0002',
                          nombre='Juan',
                          cuit='30349342406',
                          rubro='Autopartista')
        usuario.save()

        #Creo un presupuesto sin fecha de aceptacion desde el formulario web
        vals = {
            'codigo': '0002',
            'fecha_solicitado': (timezone.now() -
                              datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_realizado': (timezone.now() -
                             datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'usuario': usuario.id,
            'estado': 'borrador',
        }
        response = self.client.post(reverse('adm:presup-create'), vals)
        self.assertEqual(response.status_code, 200)
        presup = Presupuesto.objects.get(codigo='0002')
        self.assertEqual(presup.estado, 'borrador')

    def test_perm_required_create(self):
        """
        Solo los usuarios logueados y  con permisos de creacion en presupuestos
        pueden crear presupuestos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('adm:presup-create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('adm:presup-create'), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_lab_env()
        response = self.client.get(reverse('adm:presup-create'))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('adm:presup-create'), {})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_update(self):
        """
        Solo los usuarios logueados y  con permisos de modificacion en
        presupuestos pueden modificar presupuestos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('adm:presup-update',
                                           kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('adm:presup-update',
                                            kwargs={'pk': '1'}), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_lab_env()
        response = self.client.get(reverse('adm:presup-update',
                                           kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('adm:presup-update',
                                            kwargs={'pk': '1'}), {})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_delete(self):
        """
        Solo los usuarios logueados y  con permisos de eliminacion en
        presupuestos pueden eliminar presupuestos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('adm:presup-list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('adm:presup-list'),
                                            {'Eliminar': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_lab_env()
        response = self.client.post(reverse('adm:presup-list'),
                                            {'Eliminar': '1'})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_finish(self):
        """
        Solo los usuarios logueados y  con permisos de finalizacion en
        presupuestos pueden finalizar presupuestos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('adm:presup-list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('adm:presup-list'),
                                            {'Finalizar': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_lab_env()
        response = self.client.post(reverse('adm:presup-list'),
                                            {'Finalizar': '1'})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_cancel(self):
        """
        Solo los usuarios logueados y  con permisos de cancelacion en
        presupuestos pueden cancelar presupuestos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('adm:presup-list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('adm:presup-list'),
                                            {'Cancelar': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_lab_env()
        response = self.client.post(reverse('adm:presup-list'),
                                            {'Cancelar': '1'})
        self.assertEqual(response.status_code, 403)
