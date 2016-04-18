# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from .forms import ProfileForm
from django.core.urlresolvers import reverse_lazy


def is_member(user, groupName):
    return user.groups.filter(name=groupName).exists()


@login_required
def index(request):
    user = request.user
    #Chequeo el grupo al que pertenece el usuario
    if is_member(user, 'Administracion'):
        return redirect('adm/presup')
    elif is_member(user, 'LIA'):
        return redirect('lab/turnos/LIA')
    elif is_member(user, 'LIM1'):
        return redirect('lab/turnos/LIM1')
    elif is_member(user, 'LIM2'):
        return redirect('lab/turnos/LIM2')
    elif is_member(user, 'LIM3'):
        return redirect('lab/turnos/LIM3')
    elif is_member(user, 'LIM6'):
        return redirect('lab/turnos/LIM6')
    elif is_member(user, 'EXT'):
        return redirect('lab/turnos/EXT')
    elif is_member(user, 'SIS'):
        return redirect('lab/turnos/SIS')
    elif is_member(user, 'DES'):
        return redirect('lab/turnos/DES')
    return redirect('adm/presup')


class ProfileView(UpdateView):
    model = User
    template_name = 'intiSoft/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('index')
    #slug_url_kwarg = 'username'
    #slug_field = 'username'

