from django import forms
from django.db import models
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


CODE_PREFIXES = {
    'sector': 'SEC',
    'sedeeducativa': 'SED',
    'cargo': 'CAR',
    'rol': 'ROL',
    'comitesede': 'COM',
    'hitomantenimiento': 'HIT',
    'tiposervicio': 'TIP',
    'subtiposervicio': 'SUB',
    'trimestre': 'TRI',
    'metamantenimiento': 'MET',
    'evidenciamantenimiento': 'EVI',
}


def generar_codigo(model):
    """Genera un código único para modelos que tienen el campo codigo."""
    prefix = CODE_PREFIXES.get(model._meta.model_name, model._meta.model_name[:3].upper())
    base = f'{prefix}-'
    numero = model.objects.filter(codigo__startswith=base).count() + 1
    codigo = f'{base}{numero:03d}'
    while model.objects.filter(codigo=codigo).exists():
        numero += 1
        codigo = f'{base}{numero:03d}'
    return codigo


class CrudContextMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Comparte contexto y navegación para cualquier modelo del sistema."""

    crud_namespace = ''
    crud_name = ''
    form_class = None
    crud_action = 'view'

    def get_permission_required(self):
        return (
            f'{self.model._meta.app_label}.'
            f'{self.crud_action}_{self.model._meta.model_name}',
        )

    def get_form_class(self):
        if getattr(self, 'form_class', None):
            form_class = self.form_class
        else:
            form_class = modelform_factory(self.model, fields='__all__')
        if 'codigo' in form_class.base_fields:
            form_class.base_fields = form_class.base_fields.copy()
            form_class.base_fields.pop('codigo')
        for field in self.model._meta.fields:
            if field.name in form_class.base_fields and isinstance(field, models.DateField):
                form_class.base_fields[field.name].widget = forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={'type': 'date'},
                )
        return form_class

    def get_crud_context(self):
        return {
            'crud_title': self.model._meta.verbose_name_plural.title(),
            'crud_name': self.crud_name,
            'crud_namespace': self.crud_namespace,
            'list_url_name': f'{self.crud_name}_list',
            'detail_url_name': f'{self.crud_name}_detail',
            'create_url_name': f'{self.crud_name}_create',
            'update_url_name': f'{self.crud_name}_update',
            'delete_url_name': f'{self.crud_name}_delete',
            'can_add': self.request.user.has_perm(
                f'{self.model._meta.app_label}.add_{self.model._meta.model_name}'
            ),
            'can_change': self.request.user.has_perm(
                f'{self.model._meta.app_label}.change_{self.model._meta.model_name}'
            ),
            'can_delete': self.request.user.has_perm(
                f'{self.model._meta.app_label}.delete_{self.model._meta.model_name}'
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_crud_context())
        return context

    def get_success_url(self):
        return reverse(
            f'{self.crud_namespace}:{self.crud_name}_detail',
            kwargs={'pk': self.object.pk},
        )


class CrudListView(CrudContextMixin, ListView):
    context_object_name = 'objects'
    template_name = 'crud/list.html'


class CrudDetailView(CrudContextMixin, DetailView):
    context_object_name = 'object'
    template_name = 'crud/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_rows'] = [
            (field.verbose_name.title(), getattr(self.object, field.name))
            for field in self.object._meta.fields
        ]
        return context


class CrudCreateView(CrudContextMixin, CreateView):
    template_name = 'crud/form.html'
    crud_action = 'add'

    def form_valid(self, form):
        if hasattr(self.model, 'codigo'):
            form.instance.codigo = generar_codigo(self.model)
        return super().form_valid(form)


class CrudUpdateView(CrudContextMixin, UpdateView):
    template_name = 'crud/form.html'
    crud_action = 'change'


class CrudDeleteView(CrudContextMixin, DeleteView):
    template_name = 'crud/confirm_delete.html'
    crud_action = 'delete'

    def post(self, request, *args, **kwargs):
        """Elimina directamente tras la confirmación del formulario."""
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            f'{self.crud_namespace}:{self.crud_name}_list',
        )
