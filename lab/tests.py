from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Presupuesto, Usuario, OfertaTec, Turno
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, Group, User


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


def get_or_create_LIA_group():
    group, created = Group.objects.get_or_create(name='LIA')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'LIA' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_LIM1_group():
    group, created = Group.objects.get_or_create(name='LIM1')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'LIM1' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_LIM2_group():
    group, created = Group.objects.get_or_create(name='LIM2')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'LIM2' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_LIM3_group():
    group, created = Group.objects.get_or_create(name='LIM3')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'LIM3' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_LIM6_group():
    group, created = Group.objects.get_or_create(name='LIM6')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'LIM6' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_EXT_group():
    group, created = Group.objects.get_or_create(name='EXT')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'EXT' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_SIS_group():
    group, created = Group.objects.get_or_create(name='SIS')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'SIS' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_DES_group():
    group, created = Group.objects.get_or_create(name='DES')
    for p in Permission.objects.filter(content_type__app_label='lab'):
        if 'DES' in p.natural_key()[0]:
            group.permissions.add(p)
    return group


def get_or_create_other_group():
    group, created = Group.objects.get_or_create(name='Otros')
    return group


def create_adm_user():
    user = User.objects.create_user('admin',
                                    'admin@gmail.com',
                                    'admin')
    adm_group = get_or_create_admin_group()
    user.groups.add(adm_group)
    return user


def create_LIA_user():
    user = User.objects.create_user('LIA',
                                    'LIA@gmail.com',
                                    'LIA')
    lab_group = get_or_create_LIA_group()
    user.groups.add(lab_group)
    return user


def create_LIM1_user():
    user = User.objects.create_user('LIM1',
                                    'LIM1@gmail.com',
                                    'LIM1')
    lab_group = get_or_create_LIM1_group()
    user.groups.add(lab_group)
    return user


def create_LIM2_user():
    user = User.objects.create_user('LIM2',
                                    'LIM2@gmail.com',
                                    'LIM2')
    lab_group = get_or_create_LIM2_group()
    user.groups.add(lab_group)
    return user


def create_LIM3_user():
    user = User.objects.create_user('LIM3',
                                    'LIM3@gmail.com',
                                    'LIM3')
    lab_group = get_or_create_LIM3_group()
    user.groups.add(lab_group)
    return user


def create_LIM6_user():
    user = User.objects.create_user('LIM6',
                                    'LIM6@gmail.com',
                                    'LIM6')
    lab_group = get_or_create_LIM6_group()
    user.groups.add(lab_group)
    return user


def create_EXT_user():
    user = User.objects.create_user('EXT',
                                    'EXT@gmail.com',
                                    'EXT')
    lab_group = get_or_create_EXT_group()
    user.groups.add(lab_group)
    return user


def create_SIS_user():
    user = User.objects.create_user('SIS',
                                    'SIS@gmail.com',
                                    'SIS')
    lab_group = get_or_create_SIS_group()
    user.groups.add(lab_group)
    return user


def create_DES_user():
    user = User.objects.create_user('DES',
                                    'DES@gmail.com',
                                    'DES')
    lab_group = get_or_create_DES_group()
    user.groups.add(lab_group)
    return user


def create_other_user():
    user = User.objects.create_user('otro',
                                    'otro@gmail.com',
                                    'otro')
    other_group = get_or_create_other_group()
    user.groups.add(other_group)
    return user


class TurnoTest(TestCase):

    def setUp_adm_env(self):
        # Busco/creo un usuario del grupo 'Administracion'
        try:
            user = User.objects.get(username='admin')
        except:
            user = create_adm_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_LIA_env(self):
        # Busco/creo un usuario del grupo 'LIA'
        try:
            user = User.objects.get(username='LIA')
        except:
            user = create_LIA_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_LIM1_env(self):
        # Busco/creo un usuario del grupo 'LIM1'
        try:
            user = User.objects.get(username='LIM1')
        except:
            user = create_LIM1_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_LIM2_env(self):
        # Busco/creo un usuario del grupo 'LIM2'
        try:
            user = User.objects.get(username='LIM2')
        except:
            user = create_LIM2_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_LIM3_env(self):
        # Busco/creo un usuario del grupo 'LIM3'
        try:
            user = User.objects.get(username='LIM3')
        except:
            user = create_LIM3_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_LIM6_env(self):
        # Busco/creo un usuario del grupo 'LIM6'
        try:
            user = User.objects.get(username='LIM6')
        except:
            user = create_LIM6_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_EXT_env(self):
        # Busco/creo un usuario del grupo 'EXT'
        try:
            user = User.objects.get(username='EXT')
        except:
            user = create_EXT_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_SIS_env(self):
        # Busco/creo un usuario del grupo 'SIS'
        try:
            user = User.objects.get(username='SIS')
        except:
            user = create_SIS_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_DES_env(self):
        # Busco/creo un usuario del grupo 'DES'
        try:
            user = User.objects.get(username='DES')
        except:
            user = create_DES_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def setUp_other_env(self):
        # Busco/creo un usuario del grupo 'Otros'
        try:
            user = User.objects.get(username='otro')
        except:
            user = create_other_user()
        # Login
        self.client.login(username=user.username,
                          password=user.natural_key()[0])

    def test_passed_to_vencido(self):
        """
        El turno debe pasar a estado vencido cuando la fecha de fin es menor
        a la fecha actual. Solo se pasan a vencidos los turnos que se encuentran
        en espera o activos.
        """
        self.setUp_adm_env()

        ofertatec = {
            'proveedor': '106',
            'codigo': '1060104020000',
            'rubro': 'GESTION EMPRE. Y DE CALIDAD',
            'subrubro': 'DESARROLLO',
            'tipo_servicio': 'ASIST.TECNICA',
            'area': 'MEC',
            'detalle': 'Modelado de maquetas en 3D',
            'precio': '587'
            }

        response = self.client.post(reverse('adm:ofertatec-create'), ofertatec)
        self.assertEqual(response.status_code, 302)
        ofertatec = OfertaTec.objects.get(codigo='1060104020000')

        turno_pasado = {
            'fecha_inicio': (timezone.now() -
                         datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_fin': (timezone.now() -
                         datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'ofertatec': ofertatec.id,
            'cantidad': 1,
            'estado': 'en_espera',
            }
        response = self.client.post(reverse('lab:turnos-create'), turno_pasado)
        self.assertEqual(response.status_code, 302)

        turno_hoy = {
            'fecha_inicio': (timezone.now() -
                            datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_fin': timezone.now().strftime('%d/%m/%Y'),
            'ofertatec': ofertatec.id,
            'cantidad': 1,
            'estado': 'en_espera',
            }
        response = self.client.post(reverse('lab:turnos-create'), turno_hoy)
        self.assertEqual(response.status_code, 302)

        turno_futuro = {
            'fecha_inicio': (timezone.now() -
                            datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_fin': (timezone.now() +
                         datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'ofertatec': ofertatec.id,
            'cantidad': 1,
            'estado': 'en_espera',
            }
        response = self.client.post(reverse('lab:turnos-create'), turno_futuro)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('lab:turnos-list'))
        turno_list = response.context['turno_list']

        turno_pasado = turno_list.filter(fecha_fin=timezone.now() -
                                         datetime.timedelta(days=10))[0]
        self.assertEqual(turno_pasado.estado, 'vencido')
        turno_hoy = turno_list.filter(fecha_fin=timezone.now())[0]
        self.assertEqual(turno_hoy.estado, 'en_espera')
        turno_futuro = turno_list.filter(fecha_fin=timezone.now() +
                                         datetime.timedelta(days=10))[0]
        self.assertEqual(turno_futuro.estado, 'en_espera')

    def test_passed_to_activo_in_create(self):
        """
        El turno debe pasar a estado activo cuando se le asigna un presupuesto.
        """
        self.setUp_adm_env()

        usuario = {
            'nro_usuario': '0001',
            'nombre': 'Juan',
            'cuit': '30349342406',
            'rubro': 'Autopartista'
            }
        response = self.client.post(reverse('adm:usuarios-create'), usuario)
        self.assertEqual(response.status_code, 302)
        usuario = Usuario.objects.get(nro_usuario='0001')

        ofertatec = {
            'proveedor': '106',
            'codigo': '1060104020000',
            'rubro': 'GESTION EMPRE. Y DE CALIDAD',
            'subrubro': 'DESARROLLO',
            'tipo_servicio': 'ASIST.TECNICA',
            'area': 'MEC',
            'detalle': 'Modelado de maquetas en 3D',
            'precio': '587'
            }
        response = self.client.post(reverse('adm:ofertatec-create'), ofertatec)
        self.assertEqual(response.status_code, 302)
        ofertatec = OfertaTec.objects.get(codigo='1060104020000')

        #Caso en que el presupuesto asociado no esta aceptado todavia
        presupuesto_na = {
            'codigo': '0001',
            'fecha_solicitado': (timezone.now() -
                              datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'usuario': usuario.id,
            'estado': 'borrador',
            }
        response = self.client.post(reverse('adm:presup-create'),
                                    presupuesto_na)
        self.assertEqual(response.status_code, 302)
        presupuesto_na = Presupuesto.objects.get(codigo='0001')
        self.assertEqual(presupuesto_na.estado, 'borrador')

        #Caso en que el presupuesto asociado ya ha sido aceptado
        presupuesto_a = {
            'codigo': '0002',
            'fecha_solicitado': (timezone.now() -
                              datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_realizado': (timezone.now() -
                             datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_aceptado': (timezone.now() -
                            datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
            'usuario': usuario.id,
            'estado': 'borrador',
            }
        response = self.client.post(reverse('adm:presup-create'), presupuesto_a)
        self.assertEqual(response.status_code, 302)
        presupuesto_a = Presupuesto.objects.get(codigo='0002')
        self.assertEqual(presupuesto_a.estado, 'aceptado')

        #Creo un turno con presupuesto asociado
        vals = {
            'presupuesto': presupuesto_na.id,
            'fecha_inicio': (timezone.now() -
                              datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_fin': (timezone.now() +
                             datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'ofertatec': ofertatec.id,
            'cantidad': 1,
            'estado': 'en_espera',
        }
        response = self.client.post(reverse('lab:turnos-create'), vals)
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('lab:turnos-list'))
        turno = Turno.objects.get(presupuesto_id=presupuesto_na.id)
        self.assertEqual(turno.estado, 'en_espera')

        vals = {
            'presupuesto': presupuesto_a.id,
            'fecha_inicio': (timezone.now() -
                              datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_fin': (timezone.now() +
                             datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'ofertatec': ofertatec.id,
            'cantidad': 1,
            'estado': 'en_espera',
        }
        response = self.client.post(reverse('lab:turnos-create'), vals)
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('lab:turnos-list'))
        turno = Turno.objects.get(presupuesto_id=presupuesto_a.id)
        self.assertEqual(turno.estado, 'activo')

    def test_init_state_en_espera(self):
        """
        El turno debe estar en estado en_espera cuando se crea sin un
        presupuesto asociado.
        """
        self.setUp_adm_env()

        ofertatec = {
            'proveedor': '106',
            'codigo': '10601040200001',
            'rubro': 'GESTION EMPRE. Y DE CALIDAD',
            'subrubro': 'DESARROLLO',
            'tipo_servicio': 'ASIST.TECNICA',
            'area': 'MEC',
            'detalle': 'Modelado de maquetas en 3D',
            'precio': '587'
            }
        response = self.client.post(reverse('adm:ofertatec-create'), ofertatec)
        self.assertEqual(response.status_code, 302)
        ofertatec = OfertaTec.objects.get(codigo='10601040200001')

        #Creo un turno sin presupuesto asociado
        vals = {
            'fecha_inicio': (timezone.now() -
                             datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            'fecha_fin': (timezone.now() -
                             datetime.timedelta(days=10)).strftime('%d/%m/%Y'),
            #'ofertatec': ofertatec.id,
            'cantidad': 1,
            'estado': 'en_espera',
        }
        response = self.client.post(reverse('lab:LIA-create'), vals)
        self.assertEqual(response.status_code, 302)
        turno = Turno.objects.get(id='1')
        self.assertEqual(turno.estado, 'en_espera')

    def test_perm_required_create(self):
        """
        Solo los usuarios logueados y con permisos de creacion en turnos
        pueden crear turnos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('lab:turnos-create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('lab:turnos-create'), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_other_env()
        response = self.client.get(reverse('lab:turnos-create'))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('lab:turnos-create'), {})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_update(self):
        """
        Solo los usuarios logueados y con permisos de modificacion en
        turnos pueden modificar turnos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('lab:turnos-update',
                                           kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('lab:turnos-update',
                                            kwargs={'pk': '1'}), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_other_env()
        response = self.client.get(reverse('lab:turnos-update',
                                           kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('lab:turnos-update',
                                            kwargs={'pk': '1'}), {})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_delete(self):
        """
        Solo los usuarios logueados y con permisos de eliminacion en
        turnos pueden eliminar turnos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('lab:turnos-list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('lab:turnos-list'),
                                            {'Eliminar': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_other_env()
        response = self.client.post(reverse('lab:turnos-list'),
                                            {'Eliminar': '1'})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_finish(self):
        """
        Solo los usuarios logueados y con permisos de finalizacion en
        turnos pueden finalizar turnos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('lab:turnos-list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('lab:turnos-list'),
                                            {'Finalizar': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_other_env()
        response = self.client.post(reverse('lab:turnos-list'),
                                            {'Finalizar': '1'})
        self.assertEqual(response.status_code, 403)

    def test_perm_required_cancelar(self):
        """
        Solo los usuarios logueados y con permisos de cancelacion en
        turnos pueden cancelar turnos.
        """
        # Sin login (redirecciona a la pagina de login, por eso el 302)
        response = self.client.get(reverse('lab:turnos-list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        response = self.client.post(reverse('lab:turnos-list'),
                                            {'Cancelar': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
        # Sin permisos
        self.setUp_other_env()
        response = self.client.post(reverse('lab:turnos-list'),
                                            {'Cancelar': '1'})
        self.assertEqual(response.status_code, 403)