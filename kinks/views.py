import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password

from .models import KinkList, KinkListColumn, StandardKinkListEntry, CustomKinkListEntry
from editor.views import EditorView


class PasswordProtectedMixin:
    password_field = ''
    password_form_template = ''

    def bad_password(self, request):
        context = {}
        if len(self.submitted_password(request)) > 0:
            context['error_message'] = 'Incorrect password.'
        return render(request, self.password_form_template, context, status=403)

    def submitted_password(self, request):
        return request.POST.get(self.password_field, '')

    def check_password(self, request, encoded):
        return check_password(self.submitted_password(request), encoded)


class KinkListView(PasswordProtectedMixin, generic.DetailView):
    model = KinkList
    template_name = 'kinks/list.html'
    password_field = 'view-password'
    password_form_template = 'kinks/enter_view_password.html'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return self.bad_password(request)
        if len(self.object.view_password) > 0:
            if not self.check_password(request, self.object.view_password):
                return self.bad_password(request)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    post = get


class KinkListCreate(EditorView):
    def post(self, request, *args, **kwargs):
        list_data = json.loads(request.POST['kink-list-data'])
        view_password = request.POST['view-password']
        if len(view_password) > 0:
            view_password = make_password(view_password)
        else:
            view_password = ''
        edit_password = request.POST['edit-password']
        if len(edit_password) > 0:
            edit_password = make_password(edit_password)
        else:
            edit_password = ''
        kink_list = KinkList(view_password=view_password, edit_password=edit_password)
        kink_list.save()
        for column in list_data:
            column_desc = KinkListColumn[column['name'].upper()]
            entry_metadata = {'list': kink_list, 'column': column_desc.value}
            for kink in column['kinks']:
                if kink['custom']:
                    name = kink['name']
                    description = kink['description']
                    entry = CustomKinkListEntry(custom_name=name, custom_description=description, **entry_metadata)
                    entry.save()
                else:
                    kink_id = kink['id']
                    entry = StandardKinkListEntry(kink_id=kink_id, **entry_metadata)
                    entry.save()
        return HttpResponseRedirect(kink_list.get_absolute_url())


def push_edit_target(session, list_id):
    if 'edit-target' not in session:
        session['edit-target'] = [str(list_id)]
    else:
        session['edit-target'] = [*session['edit-target'], str(list_id)]


def pop_edit_target(session, list_id):
    if 'edit-target' not in session:
        raise PermissionDenied
    targets = session['edit-target']
    if str(list_id) not in targets:
        raise PermissionDenied
    targets = list(x for x in targets if x != str(list_id))
    session['edit-target'] = targets


class KinkListEdit(PasswordProtectedMixin, EditorView):
    password_field = 'edit-password'
    password_form_template = 'kinks/enter_edit_password.html'

    def get(self, request, *args, **kwargs):
        return self.bad_password(request)

    def post(self, request, *args, **kwargs):
        try:
            self.object = KinkList.objects.get(id=kwargs['pk'])
        except KinkList.DoesNotExist:
            return self.bad_password(request)
        if not self.check_password(request, self.object.edit_password):
            return self.bad_password(request)
        push_edit_target(request.session, self.object.id)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        column_data = dict((x, []) for x in KinkListColumn)
        for entry in self.object.standardkinklistentry_set.all():
            column_data[KinkListColumn(entry.column)].append({'custom': False, 'id': entry.kink_id})
        for entry in self.object.customkinklistentry_set.all():
            column_data[KinkListColumn(entry.column)].append({'custom': True, 'name': entry.custom_name, 'description': entry.custom_description})
        context['init_data'] = {
            'columns': [{'name': x.name.lower(), 'kinks': k} for x, k in column_data.items()],
            'action': reverse('kinks:kink_list_save', args=(self.object.id,)),
        }
        return context


class KinkListSave(generic.View):
    def post(self, request, *args, **kwargs):
        pop_edit_target(request.session, str(kwargs['pk']))
        list_data = json.loads(request.POST['kink-list-data'])
        kink_list = KinkList.objects.get(id=kwargs['pk'])

        # this probably could be better.
        new_standard_ids = set(k['id'] for col in list_data for k in col['kinks'] if not k['custom'])
        kink_list.standardkinklistentry_set.exclude(kink_id__in=new_standard_ids).delete()

        new_custom_names = set(k['name'] for col in list_data for k in col['kinks'] if k['custom'])
        kink_list.customkinklistentry_set.exclude(custom_name__in=new_custom_names).delete()

        for column in list_data:
            column_desc = KinkListColumn[column['name'].upper()]
            for kink in column['kinks']:
                if kink['custom']:
                    name = kink['name']
                    description = kink['description']
                    entry, _ = kink_list.customkinklistentry_set.get_or_create(
                        custom_name=name,
                        defaults={'custom_description': description, 'column': column_desc.value}
                    )
                    entry.custom_description = description
                    entry.column = column_desc.value
                    entry.save()
                else:
                    kink_id = kink['id']
                    entry, _ = kink_list.standardkinklistentry_set.get_or_create(
                        kink_id=kink_id,
                        defaults={'column': column_desc.value}
                    )
                    entry.column = column_desc.value
                    entry.save()
        return HttpResponseRedirect(kink_list.get_absolute_url())
