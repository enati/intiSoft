# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class MyAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)

        #self.base_fields['username'].widget.attrs['class'] = 'form-control'
        self.base_fields['username'].widget.attrs['placeholder'] = 'Usuario'

        #self.base_fields['password'].widget.attrs['class'] = 'form-control'
        self.base_fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs['instance']
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['type'] = 'password'
        self.fields['old_password'].widget.attrs['disabled'] = True
        self.fields['new_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password'].widget.attrs['disabled'] = True
        self.fields['cnew_password'].widget.attrs['class'] = 'form-control'
        self.fields['cnew_password'].widget.attrs['disabled'] = True

    def clean_username(self):
        return self.instance.username

    def clean_old_password(self):
        password = self.cleaned_data.get('old_password', None)
        if password:
            if not self.user.check_password(password):
                msg = "Contraseña incorrecta."
                self._errors['old_password'] = self.error_class([msg])
            else:
                return password
        return password

    def clean_cnew_password(self):
        new_password = self.cleaned_data.get('new_password', None)
        cnew_password = self.cleaned_data.get('cnew_password', None)
        if new_password != cnew_password:
            msg = "La constraseña no coincide."
            self._errors['cnew_password'] = self.error_class([msg])
        elif new_password and cnew_password:
            if len(new_password) < 2 or len(new_password) > 8:
                msg = "La contraseña debe tener entre 4 y 8 caracteres."
                self._errors['new_password'] = self.error_class([msg])
            if len(cnew_password) < 2 or len(cnew_password) > 8:
                msg = "La contraseña debe tener entre 4 y 8 caracteres."
                self._errors['cnew_password'] = self.error_class([msg])
            self.user.set_password(new_password)
        return cnew_password

    old_password = forms.CharField(max_length=10, widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(max_length=10, widget=forms.PasswordInput, required=False)
    cnew_password = forms.CharField(max_length=10, widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                 ]


