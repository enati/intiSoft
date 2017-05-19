# -*- coding: utf-8 -*-
from adm.views import *
from django.contrib.auth.models import Permission, Group, User


def create_admin_group():
    group = Group.objects.create(name='Administracion')
    for p in Permission.objects.filter(content_type__app_label__in=['adm']):
        group.permissions.add(p)
    return group


def create_lab_group(lab):
    group = Group.objects.create(name=lab)
    for p in Permission.objects.filter(content_type__model=lab):
        group.permissions.add(p)
    return group


def create_si_group():
    group = Group.objects.create(name=SI)
    for p in Permission.objects.filter(content_type__model='si'):
        group.permissions.add(p)
    return group


def create_user(name, pwd, mail, group):
    user = User.objects.create_user(name, mail, pwd)
    user.groups.add(group)
    return user
